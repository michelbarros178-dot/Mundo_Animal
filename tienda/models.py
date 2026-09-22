# tienda/models.py
from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200, default="Dirección estándar")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"

    # Método de negocio (se conserva del modelo original)
    def registrar_mascota(self, mascota):
        mascota.cliente = self
        mascota.save()
        return mascota

    def total_mascotas(self):
        return self.mascotas.count()


class Mascota(models.Model):
    ESPECIES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Roedor', 'Roedor'),
        ('Otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=30, choices=ESPECIES, default='Perro')
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(default=1)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='mascotas',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.especie} - {self.raza})"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} — ${self.precio}"

    # Método de negocio (conservado)
    def actualizar_stock(self, cantidad):
        self.stock += cantidad
        self.save()
        return self.stock


class Cita(models.Model):
    SERVICIOS = [
        ('Baño Básico', 'Baño Básico'),
        ('Baño y Peluquería', 'Baño y Peluquería'),
        ('Corte de Uñas', 'Corte de Uñas'),
    ]

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='citas'
    )
    servicio = models.CharField(max_length=50, choices=SERVICIOS)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['fecha_hora']

    def __str__(self):
        return f"{self.cliente.nombre} - {self.mascota.nombre} ({self.fecha_hora})"

    # Método de negocio (conservado)
    def confirmar(self):
        self.estado = 'Confirmada'
        self.save()
        return self.estado
