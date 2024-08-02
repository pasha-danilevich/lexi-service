from djoser.email import ActivationEmail
from config.settings import DOMAIN

class CustomActivationEmail(ActivationEmail):
    template_name = "activation.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'domain': DOMAIN,
            'site_name': 'lexi',
        })
        return context