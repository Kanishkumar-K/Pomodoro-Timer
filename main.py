import streamlit as st
from datetime import timedelta
import time
import platform

# Set initial values
work_duration = 25  # in minutes
break_duration = 5   # in minutes
is_running = False
is_break = False
time_remaining = timedelta(minutes=work_duration)
start_time = 0

# Streamlit UI layout
st.title("Pomodoro Timer App")
st.title("")
st.title("")

# Input for setting work and break durations
col1, col2 = st.columns(2)
with col1:
    work_duration = st.number_input("Set work duration (minutes)", min_value=1, value=work_duration)
    time_remaining = timedelta(minutes=work_duration)  # Update time_remaining

with col2:
    break_duration = st.number_input("Set break duration (minutes)", min_value=1, value=break_duration)

# Display countdown timer with style
time_display = st.empty()
time_display.markdown(f"<h1 style='text-align: center; color: #1f68c0;'>{work_duration:02d}:00</h1>", unsafe_allow_html=True)

# Start/Stop and Reset buttons with style
col1, col2, col3, col4 = st.columns(4)
with col2:
    if not is_running:
        if st.button("Start", key="start_button"):
            is_running = True
            start_time = time.time()

    else:
        if st.button("Pause", key="pause_button"):
            is_running = False
            time_remaining -= timedelta(seconds=time.time() - start_time)

with col3:
    if st.button("Reset", key="reset_button"):
        is_running = False
        is_break = False
        time_remaining = timedelta(minutes=work_duration)

# Countdown logic
while is_running and time_remaining.total_seconds() > 0:
    minutes, seconds = divmod(int(time_remaining.total_seconds()), 60)
    time_display.markdown(f"<h1 style='text-align: center; color: #1f68c0;'>{minutes:02d}:{seconds:02d}</h1>",
                          unsafe_allow_html=True)
    time_remaining -= timedelta(seconds=1)
    time.sleep(1)

    if time_remaining.total_seconds() <= 0:
        st.balloons()
        st.success("Session complete! Take a break.")
        
        # Play a beep sound
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 1000)  # Frequency: 1000 Hz, Duration: 1000 ms
        elif platform.system() == "Darwin":  # Mac
            import os
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        
        is_running = False
        is_break = True
        time_remaining = timedelta(minutes=break_duration)

# Break indicator and continue button
if is_break:
    st.warning("Break time! Take a moment to relax.")
    if st.button("Continue to next work session", key="continue_button"):
        is_break = False
        is_running = True
        start_time = time.time()
        time_remaining = timedelta(minutes=work_duration)

# Display final time when stopped
if not is_running and not is_break:
    minutes, seconds = divmod(int(time_remaining.total_seconds()), 60)
    time_display.markdown(f"<h1 style='text-align: center; color: #1f68c0;'>{minutes:02d}:{seconds:02d}</h1>",
                          unsafe_allow_html=True)
