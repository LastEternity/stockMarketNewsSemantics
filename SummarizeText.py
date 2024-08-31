from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration

# Initialize model and tokenizer globally to avoid reloading them each time
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text, max_length=64, num_beams=5):
    """
    Summarizes the input text using the Pegasus model.
    
    Parameters:
    - text (str): The text to summarize.
    - max_length (int): The maximum length of the summary. Default is 64.
    - num_beams (int): The number of beams for beam search. Default is 5.
    
    Returns:
    - summary (str): The generated summary of the input text.
    """
    # Tokenize the input text
    input_ids = tokenizer(text, return_tensors="pt").input_ids

    # Generate the summary using beam search
    output = model.generate(
        input_ids, 
        max_length=max_length, 
        num_beams=num_beams, 
        early_stopping=True
    )

    # Decode the output and return the summary
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    return summary

# # Example usage
# text_to_summarize = (
#     "National Commercial Bank (NCB), Saudi Arabia’s largest lender by assets, "
#     "agreed to buy rival Samba Financial Group for $15 billion in the biggest banking takeover this year. "
#     "NCB will pay 28.45 riyals ($7.58) for each Samba share, according to a statement on Sunday, valuing it at about 55.7 billion riyals. "
#     "NCB will offer 0.739 new shares for each Samba share, at the lower end of the 0.736-0.787 ratio the banks set when they signed an initial framework agreement in June. "
#     "The offer is a 3.5% premium to Samba’s Oct. 8 closing price of 27.50 riyals and about 24% higher than the level the shares traded at before the talks were made public. "
#     "Bloomberg News first reported the merger discussions. "
#     "The new bank will have total assets of more than $220 billion, creating the Gulf region’s third-largest lender. "
#     "The entity’s $46 billion market capitalization nearly matches that of Qatar National Bank QPSC, which is still the Middle East’s biggest lender with about $268 billion of assets."
# )

# summary = summarize_text(text_to_summarize, max_length=64)
# print(summary)
