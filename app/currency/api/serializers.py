from rest_framework import serializers

from currency.models import Rate, Source, ContactUs


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sale',
            'created',
            'source',
            'currency',
        )


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'source_url',
            'name',
            'note',
            'code_name',
            'source_logo',
        )


class ContactUsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        subject = 'User Contact Us'
        message = f'''
                    Request from: {validated_data['name']}
                    Reply to email: {validated_data['email_from']}
                    Subject: {validated_data['subject']}
                    Body: {validated_data['message']}
                '''
        from currency.tasks import send_mail
        send_mail.apply_async(
            kwargs={'subject': subject, 'message': message},
        )
        return ContactUs.objects.create(**validated_data)

    class Meta:
        model = ContactUs
        fields = (
            'id',
            'created',
            'name',
            'email_from',
            'subject',
            'message',
        )
