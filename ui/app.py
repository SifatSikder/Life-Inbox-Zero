import gradio as gr
import sys
import os

# Add parent directory to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.manager_agent import ManagerAgent

manager = ManagerAgent()

def process_input(text, files):
    # This is a simplified interaction. 
    # In a real app, we'd handle files and text more robustly.
    response_stream = manager.run(text)
    
    output = ""
    for chunk in response_stream:
        output += chunk + "\n"
        yield output

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Life Inbox Zero")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Chat & Command")
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Tell me what to organize...")
            file_upload = gr.File(label="Upload Files", file_count="multiple")
            btn = gr.Button("Organize My Life")
            
        with gr.Column(scale=1):
            gr.Markdown("### Card Garden")
            # Placeholder for the card garden visualization
            # In a real implementation, this would be a custom component or HTML
            card_garden = gr.HTML("<div style='padding: 20px; background: #f0f0f0; border-radius: 10px;'>Cards will appear here...</div>")
            
    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        user_message = history[-1][0]
        bot_message = ""
        for chunk in manager.run(user_message):
            bot_message += chunk + "\n"
            history[-1][1] = bot_message
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

if __name__ == "__main__":
    demo.launch()
