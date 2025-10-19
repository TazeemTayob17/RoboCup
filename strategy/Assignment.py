import math

# --- Helper Function ---
def calculate_distance(pos1, pos2):
    """
    Calculates the Euclidean distance between two points.
    """
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

# --- Main Assignment Function ---
def role_assignment(teammate_positions, formation_positions):
    """
    Assigns each teammate to a formation position using the Gale-Shapley algorithm.

    Args:
        teammate_positions: A list of numpy arrays, where each array is a player's [x, y] position.
        formation_positions: A list of numpy arrays, where each array is a formation's [x, y] position.

    Returns:
        A dictionary mapping player unum (1-5) to their assigned formation position coordinates.
    """

    num_players = len(teammate_positions)
    player_preferences = {}
    formation_preferences = {}

    # -----------------------------------------------------------#
    # Step 1: Create Preference Lists for Players and Formations
    # -----------------------------------------------------------#

    # TODO: Create player_preferences
    # For each player index (0 to 4), create a list of formation indices (0 to 4)
    # sorted from closest to farthest.
    for p_idx in range(num_players):
        # Calculate distances to all formation positions
        distances = []
        for f_idx in range(num_players):
            dist = calculate_distance(teammate_positions[p_idx], formation_positions[f_idx])
            distances.append((dist, f_idx))
        
        # Sort by distance (the first element in the tuple)
        distances.sort(key=lambda x: x[0])
        
        # Store just the sorted formation indices
        player_preferences[p_idx] = [f_idx for dist, f_idx in distances]


    # TODO: Create formation_preferences
    # For each formation index (0 to 4), create a list of player indices (0 to 4)
    # sorted from closest to farthest.
    for f_idx in range(num_players):
        # Calculate distances to all players
        distances = []
        for p_idx in range(num_players):
            dist = calculate_distance(teammate_positions[p_idx], formation_positions[f_idx])
            distances.append((dist, p_idx))
        
        # Sort by distance
        distances.sort(key=lambda x: x[0])
        
        # Store just the sorted player indices
        formation_preferences[f_idx] = [p_idx for dist, p_idx in distances]

    # -----------------------------------------------------------#
    # Step 2: Initialize the Matching Process
    # -----------------------------------------------------------#
    unmatched_players = list(range(num_players))
    current_matches = {f_idx: None for f_idx in range(num_players)} # Maps formation_idx -> player_idx

    # -----------------------------------------------------------#
    # Step 3 & 4: The Proposal Loop
    # -----------------------------------------------------------#
    
    # TODO: Implement the main while loop.
    # The loop should continue as long as 'unmatched_players' is not empty.
    while unmatched_players:
        # Get the current player to make a proposal
        proposing_player_idx = unmatched_players[0]
        
        # Get this player's top choice from their preference list
        # Hint: Use a copy or be careful, as you might modify the list
        target_formation_idx = player_preferences[proposing_player_idx][0]
        
        # Check if the target formation is currently matched
        current_partner_idx = current_matches[target_formation_idx]

        if current_partner_idx is None:
            # The formation is free. Accept the proposal.
            # 1. Assign the player to the formation.
            # 2. Remove the player from the unmatched list.
            current_matches[target_formation_idx] = proposing_player_idx
            unmatched_players.pop(0)

        else:
            # The formation is not free. It must decide.
            # Get the formation's preference list to compare.
            formation_pref_list = formation_preferences[target_formation_idx]
            
            # Find the rank of the current partner and the new proposer.
            rank_of_current_partner = formation_pref_list.index(current_partner_idx)
            rank_of_proposer = formation_pref_list.index(proposing_player_idx)

            if rank_of_proposer < rank_of_current_partner:
                # The new proposer is preferred.
                # 1. Assign the new player to the formation.
                # 2. Remove the new player from the unmatched list.
                # 3. Add the old, rejected player back to the unmatched list.
                current_matches[target_formation_idx] = proposing_player_idx
                unmatched_players.pop(0)
                unmatched_players.append(current_partner_idx)
            # else, the proposer is rejected. Nothing changes for the formation.

        # The proposing player has now proposed to this formation,
        # so remove it from their preference list so they don't propose again.
        player_preferences[proposing_player_idx].pop(0)


    # -----------------------------------------------------------#
    # Step 5: Format the Final Output
    # -----------------------------------------------------------#
    point_preferences = {}

    # TODO: Convert the 'current_matches' dictionary into the required output format.
    # The final dictionary should map unum (player_idx + 1) to the actual [x, y]
    # coordinates of their assigned formation position.
    for formation_idx, player_idx in current_matches.items():
        unum = player_idx + 1
        position = formation_positions[formation_idx]
        point_preferences[unum] = position

    return point_preferences