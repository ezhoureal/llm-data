from typing import Any
import nltk
nltk.download('punkt_tab')

def rate(text: str) -> bool:
	# Tokenize words
	words = nltk.word_tokenize(text)
	num_words = len(words)
	if num_words < 50 or num_words > 100_000:
		return False

	# Mean word length
	mean_word_len = sum(len(w) for w in words) / num_words if num_words > 0 else 0
	if mean_word_len >= 3 and mean_word_len <= 10:
		pass
	else:
		return False

	# Lines ending with ellipsis
	lines = text.splitlines()
	if len(lines) > 0:
		ellipsis_lines = sum(1 for line in lines if line.rstrip().endswith("..."))
		if ellipsis_lines / len(lines) > 0.3:
			return False

	# Words with at least one alphabetic character
	alpha_words = sum(1 for w in words if any(c.isalpha() for c in w))
	if num_words == 0 or (alpha_words / num_words) < 0.8:
		return False

	return True
    