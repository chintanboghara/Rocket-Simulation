class TutorialSystem:
    def __init__(self):
        self.tutorials = {
            'basics': {
                'title': 'Orbital Mechanics Basics',
                'steps': [
                    {
                        'title': 'What is an Orbit?',
                        'content': 'An orbit is the path a spacecraft follows around a celestial body due to gravity.',
                        'interactive': {'type': 'visualization', 'target': 'earth_orbit'}
                    },
                    {
                        'title': 'Hohmann Transfer',
                        'content': 'The most fuel-efficient way to transfer between circular orbits.',
                        'interactive': {'type': 'simulation', 'target': 'mars', 'highlight': 'transfer_orbit'}
                    },
                    {
                        'title': 'Delta-V Budget',
                        'content': 'The total velocity change needed for a mission. Lower is better!',
                        'interactive': {'type': 'calculator', 'show': 'fuel_requirements'}
                    }
                ]
            },
            'advanced': {
                'title': 'Advanced Maneuvers',
                'steps': [
                    {
                        'title': 'Gravity Assists',
                        'content': 'Use planetary gravity to gain speed without fuel.',
                        'interactive': {'type': 'flyby_demo', 'planet': 'venus'}
                    },
                    {
                        'title': 'Launch Windows',
                        'content': 'Timing is everything - planets must align for efficient transfers.',
                        'interactive': {'type': 'window_calculator', 'target': 'mars'}
                    }
                ]
            },
            'missions': {
                'title': 'Famous Space Missions',
                'steps': [
                    {
                        'title': 'Voyager Grand Tour',
                        'content': 'How Voyager used gravity assists to visit multiple planets.',
                        'interactive': {'type': 'historical', 'mission': 'voyager_2'}
                    },
                    {
                        'title': 'Mars Missions',
                        'content': 'Compare different approaches to reaching Mars.',
                        'interactive': {'type': 'comparison', 'missions': ['mars_2020', 'curiosity']}
                    }
                ]
            }
        }
        
    def get_tutorial(self, tutorial_id):
        """Get tutorial by ID"""
        return self.tutorials.get(tutorial_id)
    
    def get_all_tutorials(self):
        """Get all available tutorials"""
        return {k: {'title': v['title'], 'steps': len(v['steps'])} 
                for k, v in self.tutorials.items()}
    
    def get_step(self, tutorial_id, step_index):
        """Get specific tutorial step"""
        tutorial = self.tutorials.get(tutorial_id)
        if tutorial and 0 <= step_index < len(tutorial['steps']):
            step = tutorial['steps'][step_index]
            return {
                **step,
                'step_number': step_index + 1,
                'total_steps': len(tutorial['steps']),
                'is_last': step_index == len(tutorial['steps']) - 1
            }
        return None
    
    def generate_quiz(self, tutorial_id):
        """Generate quiz questions for tutorial"""
        quizzes = {
            'basics': [
                {
                    'question': 'What is the most fuel-efficient transfer orbit?',
                    'options': ['Direct trajectory', 'Hohmann transfer', 'Spiral orbit'],
                    'correct': 1,
                    'explanation': 'Hohmann transfers minimize energy requirements.'
                },
                {
                    'question': 'What does Delta-V measure?',
                    'options': ['Distance', 'Velocity change', 'Time'],
                    'correct': 1,
                    'explanation': 'Delta-V is the total velocity change needed for maneuvers.'
                }
            ],
            'advanced': [
                {
                    'question': 'Gravity assists can:',
                    'options': ['Only slow down spacecraft', 'Speed up or change direction', 'Only work at Jupiter'],
                    'correct': 1,
                    'explanation': 'Gravity assists can increase speed and change trajectory.'
                }
            ]
        }
        return quizzes.get(tutorial_id, [])