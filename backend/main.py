from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import turtle
import random
import os
from PIL import Image
import io
import base64
import tempfile

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnimationPrompt(BaseModel):
    prompt: str

def create_turtle_animation(prompt: str) -> str:
    try:
        # Create a turtle screen with a specific size
        screen = turtle.Screen()
        screen.setup(800, 600)
        screen.bgcolor("white")
        
        # Create a turtle
        t = turtle.Turtle()
        t.speed(0)  # Fastest speed
        t.hideturtle()  # Hide the turtle cursor
        
        # Generate random colors
        colors = ["red", "blue", "green", "purple", "orange", "pink"]
        
        # Draw based on prompt
        if "circle" in prompt.lower():
            t.pensize(3)
            t.color("blue")
            t.circle(100)
        elif "square" in prompt.lower():
            t.pensize(3)
            t.color("red")
            for _ in range(4):
                t.forward(100)
                t.right(90)
        elif "star" in prompt.lower():
            t.pensize(3)
            t.color("purple")
            for _ in range(5):
                t.forward(100)
                t.right(144)
        else:
            # Default pattern - colorful spiral
            t.pensize(2)
            for i in range(36):
                t.color(random.choice(colors))
                t.circle(50 + i)
                t.right(10)
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.eps', delete=False) as eps_file, \
             tempfile.NamedTemporaryFile(suffix='.png', delete=False) as png_file:
            
            eps_path = eps_file.name
            png_path = png_file.name
        
        # Save the drawing as an image
        canvas = screen.getcanvas()
        canvas.postscript(file=eps_path)
        
        # Convert EPS to PNG
        img = Image.open(eps_path)
        img.save(png_path)
        
        # Convert image to base64
        with open(png_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Clean up temporary files
        os.unlink(eps_path)
        os.unlink(png_path)
        
        # Close the turtle window
        screen.bye()
        
        return f"data:image/png;base64,{encoded_string}"
        
    except Exception as e:
        # Make sure to clean up the turtle window even if there's an error
        try:
            screen.bye()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Error generating animation: {str(e)}")

@app.post("/api/generate")
async def generate_video(prompt: AnimationPrompt):
    try:
        # Generate the animation using turtle
        image_data = create_turtle_animation(prompt.prompt)
        
        return {
            "status": "success",
            "message": f"Generated animation for prompt: {prompt.prompt}",
            "image_data": image_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 