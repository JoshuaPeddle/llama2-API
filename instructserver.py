from flask import Flask, request, jsonify
import os

os.environ['RANK'] = '0'
os.environ['WORLD_SIZE'] = '1'
os.environ['MASTER_ADDR'] = '127.0.0.1'
os.environ['MASTER_PORT'] = '5005'

from codellama import Llama

app = Flask(__name__)

# Load the model
generator = Llama.build(
    ckpt_dir='models/CodeLlama-7b-Instruct/',
    tokenizer_path='codellama/tokenizer.model',
    max_seq_len=1000,
    max_batch_size=1,
)

@app.route('/instruct', methods=['POST'])
def instruct():
    data = request.get_json()
    print(data)
    dialog = data['dialog']
    max_gen_len =int(data.get('max_gen_len'))
    temperature = data.get('temperature', 0.2)
    top_p = data.get('top_p', 0.9)
    
    results = generator.chat_completion(
        [[dialog]],
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p
    )
    
    return jsonify(results[0])

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=False)
