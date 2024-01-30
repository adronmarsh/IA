def reward_function(params):
    # Leer los parámetros de entrada
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']

    # Dar una recompensa muy baja por defecto
    reward = 1e-3

    # Dar una alta recompensa si ninguna rueda se sale de la pista y
    # el agente está en algún lugar entre los bordes de la pista
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1.0

    # Siempre devolver un valor flotante
    return float(reward)
