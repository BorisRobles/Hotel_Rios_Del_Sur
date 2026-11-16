"""
Protección contra ataques de fuerza bruta en el login (OWASP A07).

Si un usuario falla la contraseña 3 veces seguidas, ese usuario queda
bloqueado durante 2 minutos. Un inicio de sesión correcto reinicia el contador.

"""

import logging

from django.contrib.auth.views import LoginView
from django.core.cache import cache


MAX_INTENTOS = 3
MINUTOS_BLOQUEO = 2

logger = logging.getLogger('seguridad')


def _clave(usuario):
    return 'login_intentos:' + (usuario or '').strip().lower()


class LoginConBloqueoView(LoginView):
    template_name = 'panel/login.html'

    def post(self, request, *args, **kwargs):
        usuario = request.POST.get('username', '')

        # Si el usuario está bloqueado, ni siquiera se revisa la contraseña
        if cache.get(_clave(usuario), 0) >= MAX_INTENTOS:
            return self._respuesta_bloqueado()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Login correcto: se borra el contador de intentos fallidos
        cache.delete(_clave(form.get_user().get_username()))
        return super().form_valid(form)

    def form_invalid(self, form):
        usuario = self.request.POST.get('username', '')
        clave = _clave(usuario)

        intentos = cache.get(clave, 0) + 1
        cache.set(clave, intentos, MINUTOS_BLOQUEO * 60)

        if intentos >= MAX_INTENTOS:
            logger.warning(
                'Usuario "%s" bloqueado %s minutos tras %s intentos '
                'fallidos (IP %s)',
                usuario, MINUTOS_BLOQUEO, intentos,
                self.request.META.get('REMOTE_ADDR')
            )
            return self._respuesta_bloqueado()

        return self.render_to_response(self.get_context_data(
            form=form,
            intentos_restantes=MAX_INTENTOS - intentos,
        ))

    def _respuesta_bloqueado(self):
        formulario_vacio = self.get_form_class()(request=self.request)

        return self.render_to_response(self.get_context_data(
            form=formulario_vacio,
            bloqueado=True,
            minutos_bloqueo=MINUTOS_BLOQUEO,
        ))