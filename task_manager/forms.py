import os

from django import forms
from django.core.mail import EmailMessage

from .models import UserInterestCategory, LearningObjective


# お問い合わせフォーム
class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['name'].widget.attrs['placeholder'] = 'お名前を入力してください。'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください。'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルを入力してください。'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = f'お問い合わせ {title}'
        message = f'送信者名: {name}\nメールアドレス: {email}\nメッセージ:\n{message}'
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [os.environ.get('FROM_EMAIL')]
        cc_list = [email]

        message = EmailMessage(subject=subject, body=message, 
                               from_email=from_email, to=to_list, cc=cc_list)
        message.send()


# 興味カテゴリ追加フォーム
class AddInterestCategoryForm(forms.ModelForm):
    class Meta:
        model = UserInterestCategory
        fields = ['category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'category': '追加する興味カテゴリを選択してください。'
        }


# 学習目標設定フォーム
class SettingLearningObjectiveForm(forms.ModelForm):
    class Meta:
        model = LearningObjective
        fields = ['title', 'current_level', 'target_level']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: Python株価予測',
            }),
            'current_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例: Python基礎文法は習得済み',
            }),
            'target_level': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '詳細に記載することで、より最適な学習計画が生成されます。',
                'rows': 5,
            }),
        }
        labels = {
            'title': 'タイトル(必須)',
            'current_level': '現在のレベル(任意)',
            'target_level': '到達レベル(任意)', 
        }
