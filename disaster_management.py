import math
import sys
import threading
import mysql.connector
import numpy as np
import pandas as pd
import pygame
import requests
from sklearn.ensemble import RandomForestClassifier

# ==========================================
# STEP 1: TRAINING MACHINE LEARNING CLASSIFIER
# ==========================================
print("[INFO] Training Advanced ML Model for Smart DSS Alerts...")

df_train = pd.DataFrame({
    "Water_Level_m": [1.1, 1.6, 2.2, 2.7, 3.4, 4.1, 4.9],
    "Soil_Moisture_Pct": [30.0, 40.0, 50.0, 65.0, 75.0, 88.0, 95.0],
    "Hourly_Rainfall_mm": [1.0, 5.0, 14.0, 25.0, 35.0, 52.0, 70.0],
    "Risk_Label": [
        "SAFE",
        "SAFE",
        "WARNING",
        "WARNING",
        "RED ZONE",
        "RED ZONE",
        "RED ZONE",
    ],
})

X_train = df_train[["Water_Level_m", "Soil_Moisture_Pct", "Hourly_Rainfall_mm"]]
y_train = df_train["Risk_Label"]

ml_model = RandomForestClassifier(
    n_estimators=100, max_depth=5, random_state=42
)
ml_model.fit(X_train, y_train)
print(
    "[AI ENGINE] Model successfully trained! Ready for Data-Driven Analysis."
)


def predict_risk_from_data(water, moisture, rain):
  prediction = ml_model.predict([[water, moisture, rain]])
  return prediction[0]


# ==========================================
# STEP 2: WARNING-ONLY TELEGRAM ALERT FUNCTION
# ==========================================
def send_warning_telegram(water_level):
  def background_task():
    try:
      token = "8845824582:AAHYqtNL0tA-HAVDx9JNYTW43DJEwD0dpzo"
      chat_id = "536806501"

      message = (
          f"⚠️ EMERGENCY WARNING: Rising Hazard Detected!\nWater Level:"
          f" {water_level}m\nCitizens moving to Safe Shelters immediately!"
      )

      url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
      requests.get(url, timeout=3)
      print(
          "[SUCCESS] Telegram Warning alert successfully dispatched to phone!"
      )
    except Exception as e:
      print(f"[TELEGRAM ERROR]: {e}")

  t = threading.Thread(target=background_task)
  t.daemon = True
  t.start()


# ==========================================
# STEP 3: FETCH ANALYTICAL DATASET FROM MYSQL
# ==========================================
print("[INFO] Fetching analytical telemetry dataset from MySQL...")
try:
  conn = mysql.connector.connect(
      host="localhost", user="root", password="subha2006", database="sih_project"
  )
  query = "SELECT Water_Level_m, Soil_Moisture_Pct, Hourly_Rainfall_mm FROM hilly_weather_analytics"
  df_analytics = pd.read_sql(query, conn)
  conn.close()
  print("[SUCCESS] Analytical dataset loaded from MySQL!")
except Exception as e:
  print(f"[WARNING] DB connection failed: {e}. Using analytical dataset.")
  df_analytics = pd.DataFrame({
      "Water_Level_m": [
          1.2,
          1.5,
          1.8,
          2.3,
          2.8,
          3.2,
          3.9,
          4.5,
          3.8,
          2.5,
          1.5,
          1.2,
      ],
      "Soil_Moisture_Pct": [
          35,
          38,
          42,
          55,
          68,
          75,
          85,
          92,
          80,
          60,
          40,
          35,
      ],
      "Hourly_Rainfall_mm": [2, 4, 8, 18, 28, 38, 50, 65, 40, 20, 5, 2],
  })

# ==========================================
# STEP 4: PYGAME SETUP & PROGRAMMATIC BEEP SOUND
# ==========================================
print(
    "[INFO] Launching Pure Data-Driven DSS Simulation with Programmatic"
    " Bip Sound..."
)
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)


# Programmatically generate a loud Bip/Alarm sound using NumPy (No external file needed)
def generate_beep_sound(frequency=880, duration=0.4, volume=0.8):
  sample_rate = 44100
  t = np.linspace(0, duration, int(sample_rate * duration), False)
  # Sine wave for clean beep tone
  wave = np.sin(frequency * t * 2 * np.pi)
  # Envelope to prevent clicking noise at start/end
  envelope = np.min(
      [
          np.linspace(0, 1, len(wave)),
          np.linspace(1, 0, len(wave)),
      ],
      axis=0,
  )
  audio = (wave * envelope * 32767 * volume).astype(np.int16)
  stereo_audio = np.column_stack((audio, audio))
  return pygame.mixer.Sound(buffer=stereo_audio)


siren_sound = generate_beep_sound(frequency=880, duration=0.4, volume=0.9)
print("[SUCCESS] Bip Sound generated successfully in memory!")

WIDTH, HEIGHT = 1250, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "Disaster Management DSS: Pure Data Analysis + Programmatic Bip + Telegram"
)

clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 24)
font_small = pygame.font.SysFont(None, 16)
font_title = pygame.font.SysFont(None, 26)

# Colors
BG_COLOR = (15, 23, 42)
PANEL_COLOR = (30, 41, 59)
RIVER_BLUE = (52, 152, 219)
FLOOD_BLUE = (41, 128, 185)
ALERT_YELLOW = (241, 196, 15)
DANGER_RED = (231, 76, 60)
SAFE_GREEN = (46, 204, 113)
WHITE = (255, 255, 255)
SKIN_COLOR = (253, 203, 110)
ROCK_GRAY = (127, 140, 141)
MOUNTAIN_BROWN = (93, 64, 55)
RADAR_GREEN = (0, 255, 100)

mountain_x, mountain_y, mountain_w, mountain_h = 50, 240, 130, 460
river_x, river_y, river_w, river_h = 180, 240, 45, 460
danger_zone_x, danger_zone_y, danger_w, danger_h = 225, 240, 380, 460
shelter_x, shelter_y = 1000, 470

citizens = [
    {"x": 260, "orig_x": 260, "y": 270, "state": "normal"},
    {"x": 320, "orig_x": 320, "y": 350, "state": "normal"},
    {"x": 280, "orig_x": 280, "y": 450, "state": "normal"},
    {"x": 350, "orig_x": 350, "y": 550, "state": "normal"},
    {"x": 420, "orig_x": 420, "y": 290, "state": "normal"},
    {"x": 480, "orig_x": 480, "y": 380, "state": "normal"},
    {"x": 400, "orig_x": 400, "y": 470, "state": "normal"},
    {"x": 450, "orig_x": 450, "y": 580, "state": "normal"},
    {"x": 520, "orig_x": 520, "y": 310, "state": "normal"},
    {"x": 550, "orig_x": 550, "y": 500, "state": "normal"},
]

rocks = [
    {"x": mountain_x + 80, "y": 280, "vx": 3.0, "vy": 1.5},
    {"x": mountain_x + 90, "y": 380, "vx": 3.5, "vy": 1.8},
    {"x": mountain_x + 70, "y": 480, "vx": 3.0, "vy": 1.5},
]

frame_counter = 0
radar_angle = 0
flood_spill_width = 0
last_sent_status = "SAFE"

while True:
  screen.fill(BG_COLOR)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      if siren_sound:
        siren_sound.stop()
      pygame.quit()
      sys.exit()

  frame_counter += 1
  radar_angle = (radar_angle + 3) % 360

  row_index = (frame_counter // 150) % len(df_analytics)

  val_water = float(df_analytics["Water_Level_m"].iloc[row_index])
  val_moisture = float(df_analytics["Soil_Moisture_Pct"].iloc[row_index])
  val_rain = float(df_analytics["Hourly_Rainfall_mm"].iloc[row_index])

  current_status = predict_risk_from_data(val_water, val_moisture, val_rain)

  # ==========================================
  # BEEP SOUND & TELEGRAM TRIGGER LOGIC
  # ==========================================
  if current_status in ["WARNING", "RED ZONE"]:
    if siren_sound:
      if not pygame.mixer.get_busy():
        siren_sound.play(-1)  # Loop beep alarm continuously
  else:
    if siren_sound:
      siren_sound.stop()  # Stop instantly when status returns to SAFE

  if current_status == "WARNING":
    if last_sent_status != "WARNING":
      send_warning_telegram(val_water)
      last_sent_status = "WARNING"
  elif current_status == "SAFE":
    last_sent_status = "SAFE"

  if current_status == "SAFE":
    status_color = SAFE_GREEN
    warning_active = False
    evacuation_started = False
    red_zone_active = False
    blink_counter = 0

    impact_mins = 6.0
    evac_required_mins = 2.0
    deadline_mins = 4.0
    status_text = (
        f"🟢 STATUS SAFE: All Clear / Returning Home. [Water: {val_water}m]"
    )
    zone_color, zone_border = (40, 50, 70), (80, 100, 120)
    if flood_spill_width > 0:
      flood_spill_width = max(0, flood_spill_width - 1.5)

  elif current_status == "WARNING":
    status_color = ALERT_YELLOW
    warning_active = True
    evacuation_started = True
    red_zone_active = False
    blink_counter = (frame_counter // 25) % 2

    impact_mins = 3.0
    evac_required_mins = 1.8
    deadline_mins = 1.2

    if blink_counter == 1:
      zone_color, zone_border = ALERT_YELLOW, ALERT_YELLOW
    else:
      zone_color, zone_border = (70, 70, 40), ALERT_YELLOW

    status_text = (
        f"⚠️ WARNING: Evacuating to Safe Shelters! [Telegram Sent | Water:"
        f" {val_water}m]"
    )

  else:  # RED ZONE
    current_status = "RED ZONE"
    status_color = DANGER_RED
    warning_active = False
    evacuation_started = True
    red_zone_active = True

    impact_mins = 0.0
    evac_required_mins = 0.0
    deadline_mins = 0.0
    status_text = (
        f"🚨 RED ZONE: Critical Hazard Active in Shelters! [Water:"
        f" {val_water}m]"
    )
    zone_color, zone_border = (120, 30, 30), DANGER_RED
    if flood_spill_width < 230:
      flood_spill_width += 0.8

  impact_time_text = f"⏱️ Time to Impact: {impact_mins} mins"
  evac_time_text = f"🏃 Est. Evac Time Needed: {evac_required_mins} mins"
  deadline_text = f"⏰ Must Leave Before: {deadline_mins} mins"
  distance_text = "📍 Safe Camp Distance: 3.5 km via Corridor"

  # Top Panel UI
  top_panel_y, top_panel_h = 15, 210
  pygame.draw.rect(
      screen, PANEL_COLOR, (40, top_panel_y, 1170, top_panel_h), border_radius=10
  )
  pygame.draw.rect(
      screen,
      (70, 90, 120),
      (40, top_panel_y, 1170, top_panel_h),
      width=2,
      border_radius=10,
  )

  pygame.draw.rect(
      screen, (15, 23, 42), (60, top_panel_y + 15, 740, 38), border_radius=6
  )
  pygame.draw.rect(
      screen,
      status_color,
      (60, top_panel_y + 15, 740, 38),
      width=2,
      border_radius=6,
  )
  banner_txt = font_title.render(status_text, True, status_color)
  screen.blit(banner_txt, (72, top_panel_y + 24))

  screen.blit(
      font_large.render("📊 PURE DATA-DRIVEN DSS ENGINE", True, WHITE),
      (60, top_panel_y + 65),
  )
  screen.blit(
      font_small.render(
          "Source: MySQL Analytical Records | ML Model Analysis",
          True,
          (148, 163, 184),
      ),
      (60, top_panel_y + 92),
  )
  screen.blit(
      font_small.render(f"Water Level: {val_water}m", True, status_color),
      (60, top_panel_y + 118),
  )
  screen.blit(
      font_small.render(f"Soil Moisture: {val_moisture}%", True, status_color),
      (60, top_panel_y + 142),
  )
  screen.blit(
      font_small.render(f"Rainfall Rate: {val_rain} mm/hr", True, status_color),
      (60, top_panel_y + 166),
  )

  status_display_surface = font_small.render(
      f"AI Verdict: {current_status}", True, status_color
  )
  screen.blit(status_display_surface, (230, top_panel_y + 118))

  box_x = 380
  pygame.draw.rect(
      screen, (15, 23, 42), (box_x, top_panel_y + 105, 330, 26), border_radius=4
  )
  screen.blit(
      font_small.render(impact_time_text, True, status_color),
      (box_x + 10, top_panel_y + 110),
  )

  pygame.draw.rect(
      screen, (15, 23, 42), (box_x, top_panel_y + 135, 330, 26), border_radius=4
  )
  screen.blit(
      font_small.render(evac_time_text, True, ALERT_YELLOW),
      (box_x + 10, top_panel_y + 140),
  )

  pygame.draw.rect(
      screen, (15, 23, 42), (box_x, top_panel_y + 165, 330, 26), border_radius=4
  )
  screen.blit(
      font_small.render(deadline_text, True, DANGER_RED),
      (box_x + 10, top_panel_y + 170),
  )

  pygame.draw.rect(
      screen, (15, 23, 42), (730, top_panel_y + 165, 260, 26), border_radius=4
  )
  screen.blit(
      font_small.render(distance_text, True, SAFE_GREEN),
      (740, top_panel_y + 170),
  )

  # Radar Widget
  rx, ry = 1080, top_panel_y + 90
  r_rad = 60
  screen.blit(
      font_large.render("📡 RADAR", True, WHITE),
      (rx - 35, top_panel_y + 10),
  )
  pygame.draw.circle(screen, (10, 15, 25), (rx, ry), r_rad)
  pygame.draw.circle(screen, RADAR_GREEN, (rx, ry), r_rad, width=1)
  pygame.draw.circle(screen, RADAR_GREEN, (rx, ry), r_rad // 2, width=1)
  pygame.draw.line(screen, RADAR_GREEN, (rx - r_rad, ry), (rx + r_rad, ry))
  pygame.draw.line(screen, RADAR_GREEN, (rx, ry - r_rad), (rx, ry + r_rad))

  angle_rad = math.radians(radar_angle)
  end_x = rx + int(r_rad * math.cos(angle_rad))
  end_y = ry + int(r_rad * math.sin(angle_rad))
  pygame.draw.line(screen, (0, 255, 120), (rx, ry), (end_x, end_y), width=2)

  if current_status != "SAFE":
    pygame.draw.circle(screen, status_color, (rx - 20, ry - 15), 5)

  # Geographic Lower Section
  pygame.draw.rect(
      screen,
      MOUNTAIN_BROWN,
      (mountain_x, mountain_y, mountain_w, mountain_h),
      border_radius=8,
  )
  screen.blit(
      font_small.render("⛰️ HILL", True, WHITE),
      (mountain_x + 35, mountain_y + 10),
  )

  pygame.draw.rect(
      screen, RIVER_BLUE, (river_x, river_y, river_w, river_h)
  )
  screen.blit(font_small.render("RIVER", True, WHITE), (river_x + 3, river_y + 10))

  pygame.draw.rect(
      screen,
      zone_color,
      (danger_zone_x, danger_zone_y, danger_w, danger_h),
      border_radius=12,
  )
  pygame.draw.rect(
      screen,
      zone_border,
      (danger_zone_x, danger_zone_y, danger_w, danger_h),
      width=3,
      border_radius=12,
  )
  screen.blit(
      font_large.render("VULNERABLE HABITATION ZONE", True, WHITE),
      (danger_zone_x + 30, danger_zone_y + 15),
  )

  if red_zone_active:
    pygame.draw.rect(
        screen,
        FLOOD_BLUE,
        (
            danger_zone_x,
            danger_zone_y + 50,
            flood_spill_width,
            danger_h - 100,
        ),
    )
    screen.blit(
        font_small.render("🌊 FLOOD OVERFLOW", True, WHITE),
        (danger_zone_x + 15, danger_zone_y + 60),
    )

    for rock in rocks:
      rock["x"] += rock["vx"]
      rock["y"] += rock["vy"]
      if rock["x"] > danger_zone_x + 180:
        rock["x"] = mountain_x + 30
        rock["y"] = mountain_y + 120
      pygame.draw.circle(
          screen, ROCK_GRAY, (int(rock["x"]), int(rock["y"])), 8
      )
    screen.blit(
        font_small.render("⚠️ DEBRIS / LANDSLIDE", True, DANGER_RED),
        (danger_zone_x + 20, danger_zone_y + 110),
    )

  pygame.draw.line(
      screen,
      SAFE_GREEN,
      (danger_zone_x + danger_w, shelter_y),
      (shelter_x - 70, shelter_y),
      width=4,
  )
  screen.blit(
      font_small.render(
          "➡️ Safe Corridor (Distance: 3.5 km)", True, SAFE_GREEN
      ),
      (640, shelter_y - 25),
  )

  pygame.draw.circle(screen, SAFE_GREEN, (shelter_x, shelter_y), 70)
  pygame.draw.circle(screen, WHITE, (shelter_x, shelter_y), 70, width=3)
  screen.blit(
      font_large.render("SAFE CAMP", True, WHITE),
      (shelter_x - 55, shelter_y - 95),
  )

  for c in citizens:
    if evacuation_started:
      c["state"] = "evacuating"
      if c["x"] < shelter_x - 80:
        c["x"] += 2.5
      else:
        c["state"] = "safe"
    else:
      c["state"] = "returning"
      if c["x"] > c["orig_x"]:
        c["x"] -= 2.0
      else:
        c["x"] = c["orig_x"]
        c["state"] = "normal"

    if c["state"] == "normal":
      body_color, label = (52, 152, 219), "Citizen"
    elif c["state"] == "evacuating":
      body_color, label = DANGER_RED, "Running 🏃"
    elif c["state"] == "returning":
      body_color, label = (241, 196, 15), "Returning (All Clear) 🚶"
    else:
      body_color, label = SAFE_GREEN, "Safe 🟢"

    hx, hy = int(c["x"]), int(c["y"])
    pygame.draw.circle(screen, SKIN_COLOR, (hx, hy - 10), 5)
    pygame.draw.rect(
        screen, body_color, (hx - 4, hy - 5, 8, 14), border_radius=2
    )

    if c["x"] < shelter_x - 120 and c["x"] > c["orig_x"] + 20:
      screen.blit(font_small.render(label, True, WHITE), (hx - 20, hy - 28))

  footer_txt = font_small.render(
      "Pipeline: Pure MySQL Analytical Dataset Streaming ➡️ ML Classification"
      " ➡️ Safe Return + Programmatic Bip",
      True,
      (148, 163, 184),
  )
  screen.blit(footer_txt, (40, 720))

  pygame.display.flip()
  clock.tick(30)
