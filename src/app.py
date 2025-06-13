# Description: Deploy an agent to answer woodworking questions via the Gradio interface.
# Author: Thomas Purk
# Date: 2025-05-06
# Reference: 

import gradio as gr
from agents.woodworking_agent import woodworking_agent

expert_woodworking_agent = woodworking_agent()


""" GRADIO INTERFACE """

text_input = gr.Textbox(
    label="Expert Woodworking Assistant",
    placeholder="Enter a description of your request.",
    lines=4,
)
    
# Output element
output = gr.Textbox(label="RAG Supported Solution", lines=5)

# Create the Gradio interface
interface = gr.Interface(
    fn=expert_woodworking_agent,  # Function to process inputs
    inputs=[text_input],  # User inputs 
    outputs=[output],  # AI-generated output
    title="Gala Host Assistant: Alfred",
    description="Alfred is helping you plan a Gala at Wayne Manor.",
)

# Launch the interface with debug mode
interface.launch(debug=True)