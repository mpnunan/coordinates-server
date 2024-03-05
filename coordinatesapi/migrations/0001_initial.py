# Generated by Django 4.1.3 on 2024-03-02 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Planner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('uid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ReceptionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('number', models.IntegerField()),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WeddingPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(null=True)),
                ('read_only', models.BooleanField(null=True)),
                ('planner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wedding_planners', to='coordinatesapi.planner')),
                ('wedding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planner_weddings', to='coordinatesapi.wedding')),
            ],
        ),
        migrations.CreateModel(
            name='TableGuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_guests', to='coordinatesapi.guest')),
                ('reception_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_tables', to='coordinatesapi.receptiontable')),
            ],
        ),
        migrations.AddField(
            model_name='receptiontable',
            name='wedding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reception_tables', to='coordinatesapi.wedding'),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=200)),
                ('first_guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_problems', to='coordinatesapi.guest')),
                ('second_guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_problems', to='coordinatesapi.guest')),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantGuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.BooleanField(null=True)),
                ('party', models.BooleanField(null=True)),
                ('primary', models.BooleanField(null=True)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinatesapi.guest')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinatesapi.participant')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='wedding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coordinatesapi.wedding'),
        ),
        migrations.AddField(
            model_name='guest',
            name='wedding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guests', to='coordinatesapi.wedding'),
        ),
        migrations.CreateModel(
            name='GroupGuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest_groups', to='coordinatesapi.group')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_guests', to='coordinatesapi.guest')),
            ],
        ),
        migrations.CreateModel(
            name='Couple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='couple_firsts', to='coordinatesapi.guest')),
                ('second_guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='couple_seconds', to='coordinatesapi.guest')),
            ],
        ),
    ]
