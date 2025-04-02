# Filename: feedback_simulator_app.py

import streamlit as st
from tinytroupe import Troupe, Actor
import random
from datetime import datetime

# Extended persona classes
class Persona(Actor):
    def __init__(self, name, persona_type):
        super().__init__(name)
        self.persona_type = persona_type
        self.traits = self._set_traits()
    
    def _set_traits(self):
        # Base traits for all personas
        return {
            'verbosity': random.randint(2, 5),
            'technical_level': random.randint(1, 5),
            'positivity_bias': random.uniform(0.5, 1.5)
        }

class TechSavvyUser(Persona):
    def __init__(self, name):
        super().__init__(name, "Tech-Savvy User")
        self.traits.update({
            'technical_level': random.randint(4, 5),
            'innovation_seeking': random.uniform(1.2, 1.8)
        })
    
    def receive(self, message):
        feature = message.get('feature', '')
        verbosity = self.traits['verbosity']
        
        responses = [
            f"As a power user, I find this {feature} implementation {random.choice(['solid', 'promising', 'innovative'])}. ",
            f"This {feature} shows good technical execution. ",
            f"I appreciate the technical sophistication of this {feature}. ",
            f"The {feature} could be improved with more advanced options. "
        ]
        
        response = ' '.join(random.sample(responses, min(verbosity, len(responses))))
        
        rating = min(5, max(1, int(4 * self.traits['positivity_bias'] + random.uniform(-0.5, 0.5))))
        
        suggestions = [
            "Add API access",
            "Include customization options",
            "Provide technical documentation",
            "Allow for power user configurations"
        ]
        
        return {
            'response': response,
            'rating': rating,
            'suggestions': random.sample(suggestions, random.randint(1, 3)),
            'persona': self.persona_type
        }

class CasualUser(Persona):
    def __init__(self, name):
        super().__init__(name, "Casual User")
        self.traits.update({
            'technical_level': random.randint(1, 2),
            'simplicity_preference': random.uniform(1.5, 2.0)
        })
    
    def receive(self, message):
        feature = message.get('feature', '')
        verbosity = self.traits['verbosity']
        
        responses = [
            f"I'm not sure I completely understand this {feature} thing. ",
            f"The {feature} seems {random.choice(['complicated', 'confusing', 'nice'])}. ",
            f"Will this {feature} make the app harder to use? ",
            f"Maybe if there was a simple explanation for this {feature}. "
        ]
        
        response = ' '.join(random.sample(responses, min(verbosity, len(responses))))
        
        rating = min(5, max(1, int(2.5 * self.traits['positivity_bias'] + random.uniform(-0.5, 0.5))))
        
        suggestions = [
            "Add simple tutorial",
            "Make it more intuitive",
            "Provide clear instructions",
            "Simplify the interface"
        ]
        
        return {
            'response': response,
            'rating': rating,
            'suggestions': random.sample(suggestions, random.randint(1, 3)),
            'persona': self.persona_type
        }

class BusinessUser(Persona):
    def __init__(self, name):
        super().__init__(name, "Business User")
        self.traits.update({
            'technical_level': random.randint(3, 4),
            'productivity_focus': random.uniform(1.5, 2.0)
        })
    
    def receive(self, message):
        feature = message.get('feature', '')
        verbosity = self.traits['verbosity']
        
        responses = [
            f"From a productivity standpoint, this {feature} seems {random.choice(['useful', 'questionable', 'time-saving'])}. ",
            f"How will this {feature} impact my workflow efficiency? ",
            f"I'm evaluating this {feature} based on ROI potential. ",
            f"Does this {feature} integrate with our existing tools? "
        ]
        
        response = ' '.join(random.sample(responses, min(verbosity, len(responses))))
        
        rating = min(5, max(1, int(3.5 * self.traits['positivity_bias'] + random.uniform(-0.5, 0.5))))
        
        suggestions = [
            "Add integration options",
            "Focus on time-saving aspects",
            "Provide business case examples",
            "Include team collaboration features"
        ]
        
        return {
            'response': response,
            'rating': rating,
            'suggestions': random.sample(suggestions, random.randint(1, 3)),
            'persona': self.persona_type
        }

# Initialize the app
def main():
    st.title("AI Persona Feedback Simulator")
    st.write("Simulate user feedback for new features based on different personas")
    
    # Initialize troupe
    if 'troupe' not in st.session_state:
        st.session_state.troupe = Troupe()
        st.session_state.troupe.add_actor(TechSavvyUser("tech_user_1"))
        st.session_state.troupe.add_actor(CasualUser("casual_user_1"))
        st.session_state.troupe.add_actor(BusinessUser("business_user_1"))
        st.session_state.troupe.add_actor(TechSavvyUser("tech_user_2"))
        st.session_state.troupe.add_actor(CasualUser("casual_user_2"))
    
    # Input section
    with st.form("feature_input"):
        feature_desc = st.text_area("Feature Description", 
                                  "New dark mode toggle with scheduling options")
        persona_type = st.selectbox("Select Persona Type", 
                                  ["All", "Tech-Savvy", "Casual", "Business"])
        num_responses = st.slider("Number of Responses", 1, 10, 3)
        submitted = st.form_submit_button("Generate Feedback")
    
    if submitted:
        st.session_state.responses = []
        actors_to_query = []
        
        # Select actors based on persona filter
        if persona_type == "All":
            actors_to_query = list(st.session_state.troupe.actors.values())
        else:
            for actor in st.session_state.troupe.actors.values():
                if persona_type.lower() in actor.persona_type.lower():
                    actors_to_query.append(actor)
        
        # Get responses
        for actor in random.sample(actors_to_query, min(num_responses, len(actors_to_query))):
            response = actor.receive({
                'new feature': True,
                'feature': feature_desc
            })
            st.session_state.responses.append(response)
    
    # Display results
    if 'responses' in st.session_state and st.session_state.responses:
        st.subheader("Simulated Feedback Results")
        
        for i, response in enumerate(st.session_state.responses, 1):
            with st.expander(f"Response #{i} - {response['persona']}"):
                st.write(f"**Persona:** {response['persona']}")
                st.write(f"**Rating:** {'⭐' * response['rating']}")
                st.write(f"**Feedback:** {response['response']}")
                st.write("**Suggestions:**")
                for suggestion in response['suggestions']:
                    st.write(f"- {suggestion}")
        
        # Analysis section
        st.subheader("Aggregate Analysis")
        avg_rating = sum(r['rating'] for r in st.session_state.responses) / len(st.session_state.responses)
        st.metric("Average Rating", f"{avg_rating:.1f}/5")
        
        # Suggestion frequency
        all_suggestions = [s for r in st.session_state.responses for s in r['suggestions']]
        if all_suggestions:
            st.write("**Common Suggestions:**")
            suggestion_counts = {s: all_suggestions.count(s) for s in set(all_suggestions)}
            for suggestion, count in sorted(suggestion_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {suggestion} ({count} mentions)")
    
    # Technical report section
    st.sidebar.title("Technical Report")
    st.sidebar.write("""
    ### Simulation Algorithm Design
    - Personas are implemented as TinyTroupe Actors with trait profiles
    - Responses are generated based on persona traits (verbosity, technical level, etc.)
    - Random variation is introduced to simulate natural responses
    - Rating calculation incorporates persona bias factors
    
    ### Use Cases
    1. Pre-release feature feedback simulation
    2. Persona-specific UX testing
    3. Requirements gathering for different user segments
    4. Cost-effective alternative to user surveys
    
    ### Example Scenarios
    - Mobile app feature rollout
    - SaaS product update testing
    - Enterprise software UX validation
    """)
    
    st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
