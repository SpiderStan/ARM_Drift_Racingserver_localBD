import streamlit as st
import time
import base64
from datetime import timedelta
import pandas as pd 
import numpy as np
from PIL import Image

from  .session import fetch_post, fetch_put, fetch_get, fetch_delete
from .singletons import settings, logger

def app():

    lobby_id = st.session_state.lobby_id        
    game_id = st.session_state.game_id
    num_stages = st.session_state.num_stages
    game_track_images_set = st.session_state.game_track_images_set
    game_track_images = st.session_state.game_track_images

    result = []
    for x in range(num_stages):
        result.append(x+1)

    placeholder1 = st.empty()
    placeholder2 = st.empty()
    placeholder3 = st.empty()

    with placeholder1.container(): 
        st.write("Detailed Statistics of a Stage of Event " + str(game_id) + " of Lobby: " + str(lobby_id))

    with placeholder2.container(): 
        with st.form("my_form"):

            stage_id = st.selectbox(label="Choose Stage", options=result)

            if st.form_submit_button(f"Detailed Statistics {st.session_state.statistics_emoji}"):
                st.session_state.stage_id = stage_id
                st.session_state.game_track_images_set = game_track_images_set
                st.session_state.game_track_images = game_track_images
                st.session_state.nextpage = "statistics"
                placeholder1.empty()
                placeholder2.empty()
                placeholder3.empty()
                time.sleep(0.1)
                st.experimental_rerun()

    with placeholder3.container(): 
        if st.button(f"Back to Event {st.session_state.back_emoji}"):
            st.session_state.nextpage = "stage_racedisplay"
            placeholder1.empty()
            placeholder2.empty()
            placeholder3.empty()
            time.sleep(0.1)
            st.experimental_rerun()
