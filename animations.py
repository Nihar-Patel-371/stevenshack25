import streamlit as st
import streamlit.components.v1 as components
import time

# Function that simulates getting an AI response
def query_gpt():
    time.sleep(2)  # Simulate AI thinking time
    return "Here is the AI response!"

# Add a button to trigger the animation and response
st.markdown("# AI Thinking Animation")

# Button to start the process
if st.button("Ask AI"):
    # Display the animated box (start animation)
    components.html("""
        <html>
            <head>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>
            </head>
            <body>
                <div id="animated-box" style="width:100px; height:100px; background-color:blue;"></div>
                <script>
                    gsap.to("#animated-box", {
                        duration: 2,
                        x: 400,
                        rotation: 360,
                        repeat: -1,
                        yoyo: true
                    });
                </script>
            </body>
        </html>
    """, height=300)

    # Simulate waiting for AI response
    response = query_gpt()

    # Stop the animation once we have the response (you can customize how to stop the animation)
    components.html("""
        <html>
            <head>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>
            </head>
            <body>
                <div id="animated-box" style="width:100px; height:100px; background-color:blue;"></div>
                <script>
                    gsap.to("#animated-box", {
                        duration: 0,  // Instantly stop the animation
                        x: 0,
                        rotation: 0
                    });
                </script>
            </body>
        </html>
    """, height=300)

    # Display AI response
    st.write(response)
