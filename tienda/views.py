# tienda/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Mascota, Producto, Cita
from .forms import ClienteForm, MascotaForm, ProductoForm, CitaForm


# ============================
# PÁGINA DE INICIO
# ============================
def inicio(request):
    contexto = {
        'total_clientes': Cliente.objects.count(),
        'total_mascotas': Mascota.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_citas': Cita.objects.count(),
    }
    return render(request, 'tienda/inicio.html', contexto)


# ============================
# CLIENTES
# ============================
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'tienda/clientes/lista.html', {'clientes': clientes})


def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Cliente registrado correctamente.")
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'tienda/clientes/crear.html', {'form': form})


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Cliente actualizado.")
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'tienda/clientes/editar.html', {'form': form, 'cliente': cliente})


def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.warning(request, "⚠ Cliente eliminado.")
    return redirect('lista_clientes')


# ============================
# MASCOTAS
# ============================
def lista_mascotas(request):
    mascotas = Mascota.objects.select_related('cliente').all()
    return render(request, 'tienda/mascotas/lista.html', {'mascotas': mascotas})


def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Mascota registrada correctamente.")
            return redirect('lista_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'tienda/mascotas/crear.html', {'form': form})


def editar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Mascota actualizada.")
            return redirect('lista_mascotas')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'tienda/mascotas/editar.html', {'form': form, 'mascota': mascota})


def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    mascota.delete()
    messages.warning(request, "⚠ Mascota eliminada.")
    return redirect('lista_mascotas')


# ============================
# PRODUCTOS (INVENTARIO)
# ============================
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos/lista.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Producto agregado al inventario.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/productos/crear.html', {'form': form})


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Producto actualizado.")
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/productos/editar.html', {'form': form, 'producto': producto})


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request, "⚠ Producto eliminado.")
    return redirect('lista_productos')


# ============================
# CITAS
# ============================
def lista_citas(request):
    citas = Cita.objects.select_related('cliente', 'mascota').all()
    return render(request, 'tienda/citas/lista.html', {'citas': citas})


def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Cita agendada correctamente.")
            return redirect('lista_citas')
    else:
        form = CitaForm()
    return render(request, 'tienda/citas/crear.html', {'form': form})


def editar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "✔ Cita actualizada.")
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'tienda/citas/editar.html', {'form': form, 'cita': cita})


def eliminar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    messages.warning(request, "⚠ Cita eliminada.")
    return redirect('lista_citas')


def confirmar_cita(request, id):
    """Usa el método confirmar() del modelo — ejemplo de POO en acción."""
    cita = get_object_or_404(Cita, id=id)
    cita.confirmar()  # método del MODELO
    messages.success(request, f"✔ Cita de {cita.mascota.nombre} confirmada.")
    return redirect('lista_citas')