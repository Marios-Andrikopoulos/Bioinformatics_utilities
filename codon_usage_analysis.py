from collections import Counter

def codon_usage_analysis(dna_sequence):
    """
    Performs codon usage analysis on a DNA sequence.

    Args:
        dna_sequence: The DNA sequence as a string.

    Returns:
        A dictionary where keys are codons and values are their frequencies.
    """
    # Validate the DNA sequence (ensure it contains only A, T, G, and C)
    dna_sequence = dna_sequence.upper()
    if not set(dna_sequence).issubset("ATGC"):
        raise ValueError("Invalid DNA sequence. Sequence should contain only A, T, G, and C.")

    # Extract codons in a single step
    codons = [dna_sequence[i:i+3] for i in range(0, len(dna_sequence) - 2, 3)]

    # Count the frequency of each codon using Counter
    codon_counts = Counter(codons)

    # Calculate codon frequencies
    total_codons = sum(codon_counts.values())
    codon_frequencies = {codon: count / total_codons for codon, count in codon_counts.items()}

    return codon_frequencies

# Get DNA sequence from the user
dna_sequence = input("Enter the DNA sequence: ")

try:
    # Perform codon usage analysis
    codon_frequencies = codon_usage_analysis(dna_sequence)

    # Display the results
    print("Codon Usage Analysis:")
    for codon, frequency in codon_frequencies.items():
        print(f"{codon}: {frequency:.4f}")

except ValueError as e:
    print(e)
