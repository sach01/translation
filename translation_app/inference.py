def translate_sentence(sentence, model, vocab):
    model.eval()
    src_tensor = torch.tensor(numericalize_sentence(sentence, vocab)).unsqueeze(0)
    with torch.no_grad():
        output = model(src_tensor, src_tensor)
    translated_tokens = output.argmax(2).squeeze().tolist()
    translated_sentence = ' '.join([list(vocab.keys())[token] for token in translated_tokens])
    return translated_sentence

sentence = "This is a test"
translated_sentence = translate_sentence(sentence, model, vocab)
print(f"Translated Sentence: {translated_sentence}")
