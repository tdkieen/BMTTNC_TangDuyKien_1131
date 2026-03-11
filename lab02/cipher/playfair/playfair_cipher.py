class PlayFairCipher:

    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")
        key = "".join(dict.fromkeys(key))

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = list(key)

        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)

        return [matrix[i:i+5] for i in range(0, 25, 5)]


    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col


    def split_pairs(self, text):
        text = text.upper().replace("J", "I")
        text = "".join(filter(str.isalpha, text))

        pairs = []
        i = 0

        while i < len(text):
            a = text[i]

            if i + 1 < len(text):
                b = text[i+1]

                if a == b:
                    pairs.append(a + "X")
                    i += 1
                else:
                    pairs.append(a + b)
                    i += 2
            else:
                pairs.append(a + "X")
                i += 1

        return pairs


    def playfair_encrypt(self, plain_text, matrix):
        pairs = self.split_pairs(plain_text)
        encrypted_text = ""

        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]

            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]

            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text


    def remove_padding_x(self, text):
        result = ""

        i = 0
        while i < len(text):
            if i < len(text)-2 and text[i] == text[i+2] and text[i+1] == 'X':
                result += text[i]
                i += 2
            else:
                result += text[i]
                i += 1

        if result.endswith("X"):
            result = result[:-1]

        return result


    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        cipher_text = "".join(filter(str.isalpha, cipher_text))

        decrypted_text = ""

        pairs = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]

        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]

            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]

            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return self.remove_padding_x(decrypted_text)