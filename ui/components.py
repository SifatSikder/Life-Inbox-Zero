# This file would contain custom Gradio components or helper functions for the UI.
# For now, it's a placeholder.

def create_card_html(item):
    return f"""
    <div class="card">
        <h3>{item.get('title', 'Untitled')}</h3>
        <p>{item.get('category', 'Unknown')}</p>
    </div>
    """
