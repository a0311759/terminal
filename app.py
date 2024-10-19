import streamlit as st
import pexpect
import os

# Initialize session state for storing the current working directory, output history, and command
if 'current_dir' not in st.session_state:
    st.session_state.current_dir = os.getcwd()

if 'output_history' not in st.session_state:
    st.session_state.output_history = ""

if 'command' not in st.session_state:
    st.session_state.command = ""

# Input field for user to enter a command
command = st.text_input("Enter a command (e.g., ls, cd, mkdir, etc.):", key="command_input", value="")

# If a command is entered
if command:
    try:
        # Store the command to session state for processing
        st.session_state.command = command

        # Split the command to handle 'cd' separately
        command_parts = command.split()

        if command_parts[0] == 'cd':
            # Change the directory
            new_dir = command_parts[1] if len(command_parts) > 1 else os.path.expanduser("~")
            os.chdir(new_dir)
            st.session_state.current_dir = os.getcwd()
            st.session_state.output_history += f"\nChanged directory to: {st.session_state.current_dir}\n"
        else:
            # Execute the command using pexpect
            child = pexpect.spawn(command, cwd=st.session_state.current_dir, encoding='utf-8', timeout=10)
            child.expect(pexpect.EOF)
            output = child.before
            
            # Append the result to output history
            if output:
                st.session_state.output_history += f"\n{output}\n"
            else:
                st.session_state.output_history += "\nNo output received.\n"

        # Clear the command input field after hitting Enter
        st.session_state.command = ""

    except Exception as e:
        st.session_state.output_history += f"\nAn error occurred: {e}\n"

# Display the output history in paragraphs
st.write(st.session_state.output_history)

# Clear the input field by resetting its value
st.session_state.command = ""  # Reset the command input field
