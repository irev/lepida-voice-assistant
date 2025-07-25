class NumberToText:
    """
    Mengubah angka integer menjadi representasi kata dalam Bahasa Indonesia.
    Mendukung angka dari 0 sampai 999.999.999.
    """

    units = [
        "nol", "satu", "dua", "tiga", "empat", "lima", "enam",
        "tujuh", "delapan", "sembilan", "sepuluh", "sebelas", "dua belas",
        "tiga belas", "empat belas", "lima belas", "enam belas", "tujuh belas",
        "delapan belas", "sembilan belas"
    ]
    tens = [
        "", "", "dua puluh", "tiga puluh", "empat puluh", "lima puluh",
        "enam puluh", "tujuh puluh", "delapan puluh", "sembilan puluh"
    ]
    thousands = [
        "", "ribu", "juta"
    ]

    @classmethod
    def chunk_to_text(cls, n):
        if n == 0:
            return ""
        elif n < 12:
            return cls.units[n]
        elif n < 20:
            return cls.units[n % 10] + " belas"
        elif n < 100:
            return cls.tens[n // 10] + ("" if n % 10 == 0 else " " + cls.units[n % 10])
        else:
            if n // 100 == 1:
                prefix = "seratus"
            else:
                prefix = cls.units[n // 100] + " ratus"
            return prefix + ("" if n % 100 == 0 else " " + cls.chunk_to_text(n % 100))

    @classmethod
    def convert(cls, number):
        if not isinstance(number, int):
            raise ValueError("Input harus berupa integer.")
        if number < 0 or number > 999_999_999:
            raise ValueError("Angka di luar jangkauan yang didukung (0-999.999.999).")

        if number == 0:
            return cls.units[0]

        words = []
        num = number
        for idx, thousand in enumerate(cls.thousands):
            n = num % 1000
            if n != 0:
                chunk = cls.chunk_to_text(n)
                if thousand:
                    if idx == 1 and n == 1:
                        chunk = "seribu"
                    else:
                        chunk += " " + thousand
                words.insert(0, chunk)
            num //= 1000
            if num == 0:
                break

        return ", ".join(words)

# Convenience function for easy usage
def convert(number):
    """
    Convert number to Indonesian text representation.
    
    Args:
        number: Integer or string number to convert
        
    Returns:
        String representation in Indonesian
    """
    if isinstance(number, str):
        try:
            number = int(number)
        except ValueError:
            return str(number)  # Return original if not a valid number
    
    return NumberToText.convert(number)

# Contoh penggunaan:
# print(NumberToText.number_to_text(1234567))  # "satu juta, dua ratus tiga puluh empat ribu, lima ratus enam puluh tujuh"
# print(convert("12"))  # "dua belas"