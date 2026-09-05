from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('paginas', '0004_agendamento_status')]
    operations = [migrations.AlterField(
        model_name='agendamento', name='status',
        field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('ACEITO', 'Aceito'), ('RECUSADO', 'Recusado'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')], default='PENDENTE', max_length=10),
    )]
