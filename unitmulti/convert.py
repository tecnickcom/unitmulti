"""Convert units to SI and IEC multiples and submultiples."""


class Convert(object):
    """Methods to convert units to SI and IEC multiples and submultiples."""

    SI_STEP = 10**3   # (1000) : multiplication factor for SI (International System) units
    IEC_STEP = 2**10  # (1024) : multiplication factor for IEC (International Electrotechnical Commission) units

    UNIT_MULTIPLE = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']     # prefixes for multiples
    UNIT_SUBMULTIPLE = ['', 'm', 'u', 'n', 'p', 'f', 'a', 'z', 'y']  # prefixes for submultiples

    PRECISION = 3  # number of decimal places to keep

    def get_value_multiple(self, value, step):
        """Returns the multiple and prefix of the input value.

            Parameters
            ----------
            value : number
                value in base unit
            step : multiple base step (i.e. 1000 for SI and 1024 for IEC)
                value in base unit

            Returns
            -------
            value : float
                multiple of the input value
            prefix : string
                unit prefix
        """
        value = float(value)
        prefix = ''
        for prefix in self.UNIT_MULTIPLE:
            if value < step:
                break
            if prefix != 'Y':
                value = value / step
        return round(value, self.PRECISION), prefix

    def get_iec_value_multiple(self, value):
        """Returns the IEC multiple and prefix of the input value.

            Parameters
            ----------
            value : number
                value in base unit

            Returns
            -------
            value : float
                multiple of the input value
            unit : string
                unit with multiple prefix
        """
        num, unit = self.get_value_multiple(value, self.IEC_STEP)
        if unit == '':
            return num, 'B'
        return num, '{0}iB'.format(unit)

    def get_si_value_multiple(self, value, base_unit):
        """Returns the SI multiple and prefix of the input value.

            Parameters
            ----------
            value : number
                value in base unit
            base_unit : string
                base unit (i.e. s for seconds)

            Returns
            -------
            value : float
                multiple of the input value
            unit : string
                unit with multiple prefix
        """
        num, unit = self.get_value_multiple(value, self.SI_STEP)
        return num, '{0}{1}'.format(unit, base_unit)

    def get_value_submultiple(self, value, base_unit):
        """Returns the submultiple and prefix of the input value.

            Parameters
            ----------
            value : number
                value in base unit
            base_unit : string
                base unit (i.e. s for seconds)

            Returns
            -------
            value : float
                multiple of the input value
            unit : string
                unit with submultiple prefix
        """
        value = float(value)
        if value == 0:
            return value, base_unit
        prefix = ''
        for prefix in self.UNIT_SUBMULTIPLE:
            if value >= 1:
                break
            if prefix != 'y':
                value = value * self.SI_STEP
        return round(value, self.PRECISION), '{0}{1}'.format(prefix, base_unit)

    @staticmethod
    def format_unit_value(value, unit):
        """Print the value and unit in human-readable format.

            Parameters
            ----------
            value : number
                value
            unit : string
                unit including multiple/submultiple prefix (e.g. 'KiB')

            Returns
            -------
            string
                value with unit
        """
        if unit == 'B':
            return '{0:5.0f} {1}'.format(value, unit)
        return '{0:5.1f} {1}'.format(value, unit)
