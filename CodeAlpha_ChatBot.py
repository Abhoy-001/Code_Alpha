from tkinter import *
from datetime import datetime
# window
app = Tk()
app.title("--->>>ChatBot")
app.geometry("500x600+500+150")
app.configure(bg="#07439C") 

def draw_bubble_shape(canvas, x1, y1, x2, y2, r, **kwargs):
    pts = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
    return canvas.create_polygon(pts, **kwargs, smooth=True)

last_y = 15
def post_message(txt, is_user=True):
    global last_y
    
    bg = "#0055FF" if is_user else "#CFDDE7" 
    fg = "white" if is_user else "#0A0A0A"
    
    temp = chat_canvas.create_text(0, 0, text=txt, font=("Segoe UI", 11), width=260)
    bounds = chat_canvas.bbox(temp)
    w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
    chat_canvas.delete(temp) 

    x_pos = 460 - w - 20 if is_user else 15

    txt_id = chat_canvas.create_text(x_pos + 12, last_y + 10, text=txt, anchor="nw", font=("Segoe UI", 11), fill=fg, width=260)
    box_bounds = chat_canvas.bbox(txt_id)
    
    bubble_id = draw_bubble_shape(chat_canvas, box_bounds[0]-12, box_bounds[1]-8, box_bounds[2]+12, box_bounds[3]+8, 12, fill=bg)
    chat_canvas.tag_lower(bubble_id, txt_id)
    
    last_y = box_bounds[3] + 20
    chat_canvas.config(scrollregion=chat_canvas.bbox("all"))
    chat_canvas.yview_moveto(1.0)

def run_chat():
    prompt = user_input.get().strip()
    if not prompt:
        return
        
    post_message(prompt, is_user=True)
    user_input.delete(0, END)
    
    query = prompt.lower()
    if any(greet in query for greet in ["hi", "hello", "hey"]):
        reply = "Hey there! How's your day going?"
    elif any(word in query for word in ["good", "fine", "great"]):
        reply = "That's awesome! I love to hear it."
    elif any(word in query for word in["how are you","about you"]):
        reply = "I'm doing fantastic, thank you! Ready to help."
    elif "time" in query:
        reply = f"It's currently {datetime.now().strftime('%I:%M %p')}."
    elif any(thanks in query for thanks in ["thank", "thanks"]):
        reply = "No problem at all! Happy to help."
    elif any(bye in query for bye in ["bye", "see you","goodbye"]):
        reply = "Catch you later! Have a wonderful day."
    else:
        reply = "I'm still learning! Could you try saying that a different way?"

    app.after(400, lambda: post_message(reply, is_user=False))

ui_frame = Frame(app, bg="black")
ui_frame.place(x=10, y=10, width=480, height=490)

chat_canvas = Canvas(ui_frame, bg="#031446", highlightthickness=0)
scroller = Scrollbar(ui_frame, command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scroller.set)

scroller.pack(side=RIGHT, fill=Y)
chat_canvas.pack(side=LEFT, fill=BOTH, expand=True)

user_input = Entry(app, bg="#FFFFFF", fg="#333333", font=("Segoe UI", 12), relief=FLAT, insertbackground="#333333")
user_input.place(x=15, y=520, width=370, height=40)
user_input.focus_set()

send_btn = Button(app, text="SEND", bg="#255BB9", fg="white", font=("Segoe UI", 10, "bold"), relief=FLAT, command=run_chat, cursor="hand2")
send_btn.place(x=395, y=520, width=90, height=40)

app.bind('<Return>', lambda event: run_chat())
def initial_greeting():
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    post_message(f"{greeting}\nHow can I assist you today?", is_user=False)
app.after(500, initial_greeting)

app.mainloop()
