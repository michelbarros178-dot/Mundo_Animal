# tienda/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Mascota, Producto, Cita


# ==========================================================
# CONFIGURACIÓN GLOBAL DEL ADMIN
# ==========================================================
admin.site.site_header = "🐾 Mundo Animal — Administración"
admin.site.site_title = "Mundo Animal Admin"
admin.site.index_title = "Panel de gestión interno"


# ==========================================================
# CLIENTE
# ==========================================================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'direccion', 'mostrar_mascotas', 'creado_en')
    list_filter = ('creado_en',)
    search_fields = ('nombre', 'telefono', 'direccion')
    ordering = ('nombre',)
    date_hierarchy = 'creado_en'
    readonly_fields = ('creado_en',)

    fieldsets = (
        ('Datos personales', {
            'fields': ('nombre', 'telefono', 'direccion')
        }),
        ('Información del sistema', {
            'fields': ('creado_en',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Mascotas', ordering='mascotas')
    def mostrar_mascotas(self, obj):
        total = obj.total_mascotas()
        color = '#10b981' if total > 0 else '#94a3b8'
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">🐾 {}</span>',
            color, total
        )


# ==========================================================
# MASCOTA (Inline dentro de Cliente)
# ==========================================================
class MascotaInline(admin.TabularInline):
    model = Mascota
    extra = 0
    fields = ('nombre', 'especie', 'raza', 'edad')
    show_change_link = True


# Re-registrar Cliente con el inline
# (Hay que quitar el registro anterior y volver a registrarlo)
admin.site.unregister(Cliente)


@admin.register(Cliente)
class ClienteConMascotasAdmin(ClienteAdmin):
    inlines = [MascotaInline]


# ==========================================================
# MASCOTA
# ==========================================================
@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'edad', 'cliente_link')
    list_filter = ('especie', 'edad')
    search_fields = ('nombre', 'raza', 'cliente__nombre')
    ordering = ('nombre',)
    list_select_related = ('cliente',)
    autocomplete_fields = ('cliente',)

    fieldsets = (
        ('Datos de la mascota', {
            'fields': ('nombre', 'especie', 'raza', 'edad')
        }),
        ('Dueño', {
            'fields': ('cliente',)
        }),
    )

    @admin.display(description='Dueño', ordering='cliente__nombre')
    def cliente_link(self, obj):
        if obj.cliente:
            url = f'/admin/tienda/cliente/{obj.cliente.id}/change/'
            return format_html('<a href="{}">👤 {}</a>', url, obj.cliente.nombre)
        return '—'


# ==========================================================
# PRODUCTO
# ==========================================================
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_formateado', 'stock_con_color', 'creado_en')
    list_filter = ('creado_en',)
    search_fields = ('nombre',)
    ordering = ('nombre',) 
    readonly_fields = ('creado_en',)

    fieldsets = (
        ('Información del producto', {
            'fields': ('nombre', 'precio', 'stock')
        }),
        ('Registro', {
            'fields': ('creado_en',),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Precio', ordering='precio')
    def precio_formateado(self, obj):
        return format_html(
            '<strong style="color:#059669;">${:,.0f}</strong>',
            obj.precio
        )

    @admin.display(description='Stock', ordering='stock')
    def stock_con_color(self, obj):
        if obj.stock > 5:
            bg, icon = '#d1fae5', '✅'
            color = '#059669'
        elif obj.stock > 0:
            bg, icon = '#fed7aa', '⚠️'
            color = '#c2410c'
        else:
            bg, icon = '#fee2e2', '❌'
            color = '#b91c1c'

        return format_html(
            '<span style="background:{};color:{};padding:4px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">'
            '{} {}</span>',
            bg, color, icon, obj.stock
        )


# ==========================================================
# CITA
# ==========================================================
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente_link', 'mascota_link', 'servicio', 'fecha_hora', 'estado_badge')
    list_filter = ('estado', 'servicio', 'fecha_hora')
    search_fields = ('cliente__nombre', 'mascota__nombre')
    ordering = ('-fecha_hora',)
    date_hierarchy = 'fecha_hora'
    list_select_related = ('cliente', 'mascota')
    autocomplete_fields = ('cliente', 'mascota')
    actions = ['confirmar_citas', 'cancelar_citas']

    fieldsets = (
        ('Información de la cita', {
            'fields': ('cliente', 'mascota', 'servicio', 'fecha_hora')
        }),
        ('Estado', {
            'fields': ('estado',),
            'description': 'Usa "Confirmada" cuando el cliente confirme la asistencia.'
        }),
    )

    @admin.display(description='Cliente', ordering='cliente__nombre')
    def cliente_link(self, obj):
        url = f'/admin/tienda/cliente/{obj.cliente.id}/change/'
        return format_html('<a href="{}">👤 {}</a>', url, obj.cliente.nombre)

    @admin.display(description='Mascota', ordering='mascota__nombre')
    def mascota_link(self, obj):
        url = f'/admin/tienda/mascota/{obj.mascota.id}/change/'
        return format_html('<a href="{}">🐾 {}</a>', url, obj.mascota.nombre)

    @admin.display(description='Estado', ordering='estado')
    def estado_badge(self, obj):
        colores = {
            'Pendiente':  ('#fed7aa', '#c2410c', '⏳'),
            'Confirmada': ('#d1fae5', '#059669', '✅'),
            'Cancelada':  ('#fee2e2', '#b91c1c', '❌'),
        }
        bg, color, icon = colores.get(obj.estado, ('#e2e8f0', '#334155', '•'))
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;'
            'border-radius:12px;font-size:12px;font-weight:600;">'
            '{} {}</span>',
            bg, color, icon, obj.estado
        )

    # ---------- ACCIONES MASIVAS ----------
    @admin.action(description='✅ Confirmar citas seleccionadas')
    def confirmar_citas(self, request, queryset):
        actualizadas = 0
        for cita in queryset:
            if cita.estado != 'Confirmada':
                cita.confirmar()   # método del MODELO (¡POO en acción!)
                actualizadas += 1
        self.message_user(request, f"{actualizadas} cita(s) confirmada(s).")

    @admin.action(description='❌ Cancelar citas seleccionadas')
    def cancelar_citas(self, request, queryset):
        actualizadas = queryset.update(estado='Cancelada')
        self.message_user(request, f"{actualizadas} cita(s) cancelada(s).")