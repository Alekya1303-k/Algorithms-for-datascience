# Filename: persona_simulation_init.py

from tinytroupe import Troupe, Actor
import markdown

# Define persona actors
class TechSavvyUser(Actor):
    def __init__(self, name):
        super().__init__(name)
        self.persona = "Tech-savvy early adopter"
    
    def receive(self, message):
        feature = message.get('feature', '')
        if "new feature" in message:
            return {
                'response': f"As a tech enthusiast, I find this {feature} feature intriguing. " 
                          "I appreciate the innovation but would want to see more customization options. "
                          "The implementation seems solid but could use better documentation for power users.",
                'rating': 4,
                'suggestions': ["Add advanced settings", "Improve API documentation"]
            }

class CasualUser(Actor):
    def __init__(self, name):
        super().__init__(name)
        self.persona = "Casual smartphone user"
    
    def receive(self, message):
        feature = message.get('feature', '')
        if "new feature" in message:
            return {
                'response': f"I'm not sure I understand this {feature} thing completely. "
                          "Is it going to make my phone harder to use? "
                          "Maybe if there was a simple tutorial I could follow...",
                'rating': 2,
                'suggestions': ["Add step-by-step guide", "Make it more intuitive"]
            }

# Initialize the troupe
troupe = Troupe()

# Add actors to the troupe
troupe.add_actor(TechSavvyUser("tech_user_1"))
troupe.add_actor(CasualUser("casual_user_1"))

# Simulate conversations
feature_description = "new dark mode toggle in settings"

tech_feedback = troupe.actors['tech_user_1'].receive({
    'new feature': True,
    'feature': feature_description
})

casual_feedback = troupe.actors['casual_user_1'].receive({
    'new feature': True,
    'feature': feature_description
})

# Generate markdown output
md_content = f"""
# Persona Simulation Results - Initial Draft

## Feature Tested
**{feature_description}**

## Tech-Savvy User Feedback
**Rating:** {tech_feedback['rating']}/5  
**Feedback:** {tech_feedback['response']}  
**Suggestions:** {", ".join(tech_feedback['suggestions'])}

## Casual User Feedback
**Rating:** {casual_feedback['rating']}/5  
**Feedback:** {casual_feedback['response']}  
**Suggestions:** {", ".join(casual_feedback['suggestions'])}

## Observations
- Clear difference in reception based on technical proficiency
- Both personas identified need for better documentation/guidance
- Tech user more receptive to innovation while casual user needs reassurance
"""

# Save to markdown file
with open("persona_simulation_results.md", "w") as f:
    f.write(md_content)

print("Initial persona simulation complete. Results saved to persona_simulation_results.md")
