# Main testing module for Lab 3 - Task 2
# Developer: Dmitry Melnik
# Date: May 01, 2025

from task2.text_analyzer import TextAnalyzer
from task2.file_handler import FileHandler, ArchiveHandler
from task2.utils import get_valid_input, handle_exception

def analyze_text(input_file, output_file, zip_file):
    """Analyze text and save results."""
    file_handler = FileHandler(input_file)
    output_handler = FileHandler(output_file)
    archive_handler = ArchiveHandler(output_file)

    try:
        text = file_handler.read_text()
        analyzer = TextAnalyzer(text)

        total, decl, inter, imper = analyzer.count_sentences()
        avg_sent_len = analyzer.avg_sentence_length()
        avg_word_len = analyzer.avg_word_length()
        smileys = analyzer.count_smileys()
        f_to_y_words = analyzer.find_f_to_y_words()
        prices = analyzer.extract_prices()
        short_count = analyzer.short_words()
        shortest_a = analyzer.shortest_word_ending_a()
        sorted_words = analyzer.words_by_length_desc()

        results = {
            'Total sentences': total,
            'Declarative sentences': decl,
            'Interrogative sentences': inter,
            'Imperative sentences': imper,
            'Average sentence length (words)': avg_sent_len,
            'Average word length (chars)': avg_word_len,
            'Smileys count': smileys,
            'Words with letters f-y': f_to_y_words,
            'Prices (USD, RUR, EU)': prices,
            'Words shorter than 7 chars': short_count,
            'Shortest word ending with a': shortest_a,
            'Words sorted by length (descending)': sorted_words
        }

        output_handler.save_results(results)
        archive_handler.zip_results(output_file, zip_file)
        archive_info = archive_handler.get_archive_info(zip_file)

        return results, archive_info
    except Exception as e:
        handle_exception(e)
        return None, None

def main():
    while True:
        print("\nTask 2: Text Analysis System")
        print("1. Analyze text from file")
        print("2. Back to Task Selection")
        choice = get_valid_input("Enter your choice (1-2): ", 1, 2)

        try:
            if choice == 1:
                input_file = "./task2/input.txt"
                output_file = "./task2/output.txt"
                zip_file = "./task2/output.zip"
                results, archive_info = analyze_text(input_file, output_file, zip_file)
                if results:
                    print("\nAnalysis Results:")
                    for key, value in results.items():
                        print(f"{key}: {value}")
                    print("\nArchive Info:")
                    for info in archive_info:
                        print(f"File: {info.filename}, Size: {info.file_size} bytes")
            elif choice == 2:
                break
        except Exception as e:
            handle_exception(e)

if __name__ == "__main__":
    main()