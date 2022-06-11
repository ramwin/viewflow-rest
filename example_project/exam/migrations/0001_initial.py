# Generated by Django 4.0.5 on 2022-06-11 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import viewflow_rest.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_class', viewflow_rest.fields.FlowReferenceField(verbose_name='Flow')),
                ('status', models.CharField(choices=[('NEW', '创建了'), ('STARTED', '开始了'), ('DONE', '结束了'), ('CANCELED', '取消了')], default='STARTED', max_length=15, verbose_name='状态')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
                ('finish_datetime', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(choices=[('math', 'math'), ('art', 'art')], max_length=31, verbose_name='subject')),
                ('passed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExamTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_task', viewflow_rest.fields.TaskReferenceField(verbose_name='Task')),
                ('flow_task_type', models.CharField(max_length=31, verbose_name='类型')),
                ('status', models.CharField(choices=[('NEW', '创建了'), ('STARTED', '开始了'), ('DONE', '结束了'), ('CANCELED', '取消了')], max_length=15, verbose_name='状态')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
                ('finish_datetime', models.DateTimeField(blank=True, null=True)),
                ('term', models.DateField(null=True)),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('previous', models.ManyToManyField(related_name='leading', to='exam.examtask', verbose_name='上级任务')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.examprocess')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]