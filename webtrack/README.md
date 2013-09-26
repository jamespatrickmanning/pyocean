track_web_data
===============

Sphinx website:

http://www.nefsc.noaa.gov/epd/ocean/MainPage/py/sphinx_track_web/_build/html/index.html

--'boundary.py' gets model tracks according to the spacial time and position. Adds boundary response when track hits boundary.(reflected when tracks hit coast line and stopped when tracks hit model edge)

--'circletrack_nearest.py' can get the concentric points tracks.Uses "nearest" method to get model data.(compared RungeKutta method)

--'tracknearest_surface.py' plots tracks according to the spacial time, position etc.Uses "nearest"method and control file is"ctrl_tracknearest_surface.csv"

--'web_surface.py' plots surface track on model map. Uses "RungeKutta" method to get model data.

--'web_vertical.py'plots model track with u,v,w velocities.Uses "RungeKutta" method to get model data.

--"web_vertical_behavior_circle_contour.py" plots model track with u,v,w,animal behavior velocities. Uses "RungeKutta" method to get model data.