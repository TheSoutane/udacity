from sample_players import DataPlayer
import random
import numpy as np

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation
    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.
    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def pvs_solver(self,state, depth, alpha, beta, color):
        if depth <=0 or state.terminal_test():
            return color*self.get_score(state)
        explored = []
        
        for action in state.actions():
            if action not in explored:
#                 print('not explored')
                explored.append(action)
                score = self.pvs_solver(state.result(action),depth-1,alpha,beta,-color)
            else:
#                 print('explored')
                score = self.pvs_solver(state.result(action),depth-1,alpha,alpha+1,-color)
                if alpha<score and beta>score:
                    score = self.pvs_solver(state.result(a),depth-1,alpha,beta,-color)
                    #score = -score
#             print('alpha', alpha, 'score', score)
            if alpha<score:
                alpha = score
            if alpha>=beta:
                break
        return alpha
    
    def pv_method(self,state,depth):
        print(depth)
        alpha = -np.inf
        beta = np.inf
        actions = state.actions()
        print('Check actions')
        if actions:
            best_move = actions[0]
        else:
            return None
        maximizingplayer = 1
        v = -np.inf
        
        _first_action = True
        print('loop over actions')
        for action in actions:
            print('loop')
            new_state = state.result(action)
            if _first_action:
                print('first action')
                _first_action = False
                v = max(v,self.pvs_solver(new_state,depth-1,alpha,beta,maximizingplayer))
            else:
                print('other action')
                v = max(v,self.pvs_solver(new_state,depth-1,alpha,alpha+1,maximizingplayer))
                if v>alpha:
                    v = max(v,self.pvs_solver(new_state,depth-1,alpha,beta,maximizingplayer))
            if v>alpha:
                alpha=v
                best_move=action
            print('best_move')
            print(best_move)
        return best_move
    
    def get_score(self, state):
        """computes game score according to the metric player_1_actions - player_2_actions
        """
        own_actions = state.liberties(state.locs[self.player_id])
        opp_actions = state.liberties(state.locs[1 - self.player_id])
        return len(own_actions) - len(opp_actions)     
    
    
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least
        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.
        See RandomPlayer and GreedyPlayer in sample_players for more examples.
        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        
        if state.ply_count < 2:
            print('first random')
            self.queue.put(random.choice(state.actions()))
            print('end first random')
        else:
            print('look for optimal action')  
            
            optimal_action = self.pv_method(state,6)
            print(type(random.choice(state.actions())))
            print(type(optimal_action))
            
            print('found optimal action')
            print(len(optimal_action))
            self.queue.put(optimal_action)
            print('end optimal action')
        