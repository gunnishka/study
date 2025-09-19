import math
from collections import Counter

class TextAnalyzer:
    def __init__(self, text):
        self.text = text.lower()  # Приводим к нижнему регистру для единообразия
        self.clean_text = ''.join([c for c in self.text if c.isalpha() or c.isspace()])

    def calculate_entropy(self, n=1):
        """Вычисляет энтропию для n-буквенных сочетаний"""
        if n == 1:
            sequences = list(self.clean_text)
        else:
            # Создаем n-граммы
            sequences = [self.clean_text[i:i + n] for i in range(len(self.clean_text) - n + 1)]

        counter = Counter(sequences)
        total = len(sequences)
        entropy = 0

        for count in counter.values():
            p = count / total
            entropy -= p * math.log2(p)

        return entropy

    def uniform_code_length(self, n=1):
        """Длина кода при равномерном кодировании"""
        if n == 1:
            unique_chars = len(set(self.clean_text))
        else:
            sequences = [self.clean_text[i:i + n] for i in range(len(self.clean_text) - n + 1)]
            unique_chars = len(set(sequences))

        return math.ceil(math.log2(unique_chars))

    def redundancy(self, n=1):
        """Вычисляет избыточность"""
        entropy = self.calculate_entropy(n)
        uniform_length = self.uniform_code_length(n)
        return uniform_length - entropy


class ShannonFanoEncoder:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}

    def build_codes(self, probabilities):
        """Строит коды Шеннона-Фано"""
        sorted_probs = sorted(probabilities.items(),
                              key=lambda x: x[1], reverse=True)
        self.codes = {}

        def _recursive_build(symbols, code=""):
            if len(symbols) == 1:
                self.codes[symbols[0][0]] = code
                return

            total = sum(prob for _, prob in symbols)
            cum_sum = 0
            split_idx = 0

            for i, (symbol, prob) in enumerate(symbols):
                cum_sum += prob
                if cum_sum >= total / 2:
                    split_idx = i + 1
                    break

            _recursive_build(symbols[:split_idx], code + "0")
            _recursive_build(symbols[split_idx:], code + "1")

        _recursive_build(sorted_probs)
        self.reverse_codes = {v: k for k, v in self.codes.items()}
        return self.codes

    def encode(self, text, n=1):
        """Кодирует текст с заданной длиной n-грамм"""
        if n == 1:
            sequences = list(text)
        else:
            sequences = [text[i:i + n] for i in range(0, len(text), n)]
            # Дополняем последнюю последовательность если нужно
            if len(sequences[-1]) < n:
                sequences[-1] = sequences[-1].ljust(n, ' ')

        # Вычисляем вероятности
        counter = Counter(sequences)
        total = len(sequences)
        probabilities = {k: v / total for k, v in counter.items()}

        # Строим коды
        codes = self.build_codes(probabilities)

        # Кодируем
        encoded = ''.join(codes[s] for s in sequences)

        return encoded, codes, probabilities

    def decode(self, encoded_text, n=1):
        """Декодирует текст"""
        current_code = ""
        decoded_segments = []

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_segments.append(self.reverse_codes[current_code])
                current_code = ""

        decoded_text = ''.join(decoded_segments)
        return decoded_text

    def average_code_length(self, probabilities):
        """Вычисляет среднюю длину кода"""
        avg_length = 0
        for symbol, prob in probabilities.items():
            avg_length += prob * len(self.codes[symbol])
        return avg_length

    def compression_efficiency(self, original_text, encoded_text, n=1):
        """Вычисляет эффективность сжатия"""
        if n == 1:
            original_bits = len(original_text) * 8  # ASCII
        else:
            original_bits = len(original_text) * 8

        compressed_bits = len(encoded_text)
        compression_ratio = original_bits / compressed_bits

        return compression_ratio, compressed_bits, original_bits


def main():
    # Пример текста для анализа
    text = """
    Алгоритм Шеннона-Фано является одним из первых алгоритмов сжатия данных, 
    разработанных в 1949 году. Он использует статистические свойства данных 
    для эффективного кодирования. Основная идея заключается в построении 
    префиксных кодов на основе вероятностей появления символов.
    """

    analyzer = TextAnalyzer(text)
    encoder = ShannonFanoEncoder()

    print("=" * 60)
    print("СТАТИСТИЧЕСКАЯ ОБРАБОТКА ТЕКСТА")
    print("=" * 60)

    # Анализ для однобуквенных сочетаний
    print("\n1. ОДНОБУКВЕННЫЕ СОЧЕТАНИЯ:")
    print("-" * 40)

    entropy_1 = analyzer.calculate_entropy(1)
    uniform_length_1 = analyzer.uniform_code_length(1)
    redundancy_1 = analyzer.redundancy(1)

    print(f"Энтропия: {entropy_1:.4f} бит/символ")
    print(f"Длина равномерного кода: {uniform_length_1} бит")
    print(f"Избыточность: {redundancy_1:.4f} бит")

    # Кодирование однобуквенных сочетаний
    encoded_1, codes_1, probs_1 = encoder.encode(analyzer.clean_text, 1)
    avg_length_1 = encoder.average_code_length(probs_1)
    efficiency_1, compressed_bits_1, original_bits_1 = encoder.compression_efficiency(
        analyzer.clean_text, encoded_1, 1)

    print(f"\nКоды Шеннона-Фано:")
    for symbol, code in sorted(codes_1.items()):
        print(f"'{symbol}': {code} (p={probs_1[symbol]:.4f})")

    print(f"\nСредняя длина кода: {avg_length_1:.4f} бит")
    print(f"Эффективность сжатия: {efficiency_1:.2f}:1")
    print(f"Исходный размер: {original_bits_1} бит")
    print(f"Сжатый размер: {compressed_bits_1} бит")

    # Декодирование
    decoded_1 = encoder.decode(encoded_1, 1)
    print(f"\nДекодирование успешно: {analyzer.clean_text == decoded_1}")

    # Анализ для двухбуквенных сочетаний
    print("\n\n2. ДВУХБУКВЕННЫЕ СОЧЕТАНИЯ:")
    print("-" * 40)

    entropy_2 = analyzer.calculate_entropy(2)
    uniform_length_2 = analyzer.uniform_code_length(2)
    redundancy_2 = analyzer.redundancy(2)

    print(f"Энтропия: {entropy_2:.4f} бит/символ")
    print(f"Длина равномерного кода: {uniform_length_2} бит")
    print(f"Избыточность: {redundancy_2:.4f} бит")

    # Кодирование двухбуквенных сочетаний
    encoded_2, codes_2, probs_2 = encoder.encode(analyzer.clean_text, 2)
    avg_length_2 = encoder.average_code_length(probs_2)
    efficiency_2, compressed_bits_2, original_bits_2 = encoder.compression_efficiency(
        analyzer.clean_text, encoded_2, 2)

    print(f"\nКоличество уникальных биграмм: {len(codes_2)}")
    print(f"Средняя длина кода: {avg_length_2:.4f} бит")
    print(f"Эффективность сжатия: {efficiency_2:.2f}:1")
    print(f"Исходный размер: {original_bits_2} бит")
    print(f"Сжатый размер: {compressed_bits_2} бит")

    # Декодирование
    decoded_2 = encoder.decode(encoded_2, 2)
    print(f"\nДекодирование успешно: {analyzer.clean_text == decoded_2}")

if __name__ == "__main__":
    main()
