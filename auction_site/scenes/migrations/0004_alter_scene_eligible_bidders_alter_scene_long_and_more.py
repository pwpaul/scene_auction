# Generated by Django 5.2.1 on 2025-07-15 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0003_alter_scene_options_scene_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='eligible_bidders',
            field=models.ManyToManyField(blank=True, help_text='This is an effort to make sure bidders are compatible in more sexually based scenes.<p> This is optional for scenes where sexual contact is not available.</p>', to='scenes.eligiblebidder', verbose_name='Eligible Bidders (Select All That Apply - Optional)'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='long',
            field=models.TextField(blank=True, help_text='Optional longer description, will help the auctioneer be more descriptive.', verbose_name='Long Scene Description'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='other_bidders',
            field=models.CharField(blank=True, help_text='Any other specific bidder audience not listed (I tried but you know better than I do).', max_length=200, verbose_name='Other Eligible Bidders'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='role',
            field=models.CharField(choices=[('top', 'Top'), ('bottom', 'Bottom')], help_text='Your Role in the scene', max_length=10),
        ),
        migrations.AlterField(
            model_name='scene',
            name='short',
            field=models.TextField(blank=True, help_text='Main description for the auctioneer and audience.<p> Please be explicit if sexual contact is included.  All contact is negotated before scene happens </p>', verbose_name='Short Scene Description'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='title',
            field=models.CharField(help_text='This is the title the auctioneer will use for your scene', max_length=200),
        ),
    ]
