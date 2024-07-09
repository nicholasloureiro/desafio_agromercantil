from django import forms
from .models import Posts
from yahoo_fin.stock_info import tickers_nasdaq

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['ticker', 'description']

    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'
    
    def clean_ticker(self):
        ticker = self.cleaned_data.get('ticker')
        if ticker.upper() not in tickers_nasdaq():
            raise forms.ValidationError("O ticker não está disponível.")
        return ticker
