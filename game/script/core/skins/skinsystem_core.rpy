################################################################################
## Sistema de Skins - Versión 3.0 (Integrado con Rutinas)
################################################################################
## Sistema para gestionar skins de NPCs con grupos asignados por rutina
## Cada rutina tiene un grupo de skin que controla qué sprite se muestra

################################################################################
## Grupos de Skins Oficiales
################################################################################

init python:
    
    # Grupos de skins disponibles (extensible)
    SKIN_GRUPOS = ["base", "entrenamiento", "bikini", "pijama", "ropa_interior", "vestidos"]
    
    # Diccionario global para asignar grupos de skin a rutinas
    # Formato: {npc_id: {(dia, horario): grupo_skin}}
    rutinas_skin_grupos = {}
    
    
    class Skin:
        """
        Clase que representa un skin para un NPC.
        
        Los skins pueden:
        - Pertenecer a un grupo (base, entrenamiento, etc.)
        - Tener condiciones de desbloqueo
        - Definir sprites idle y de menú para el grupo
        """
        
        def __init__(self, id, npc_id, nombre, grupo="base", descripcion="",
                condicion_desbloqueo=None, sprite_idle=None, sprite_menu=None,
                posicion=None):
            """
            Args:
                id: ID único del skin (ej: "jasmine_entrenamiento_deportiva")
                npc_id: ID del NPC al que pertenece
                nombre: Nombre visible en el menú
                grupo: Grupo del skin (ej: "base", "entrenamiento")
                descripcion: Descripción del skin
                condicion_desbloqueo: Callable que retorna bool
                sprite_idle: Ruta al sprite idle (usado en rutinas de este grupo)
                sprite_menu: Ruta al sprite para vista previa en menú
                posicion: Posición opcional para el sprite (x, y)
            """
            self.id = id
            self.npc_id = npc_id
            self.nombre = nombre
            self.grupo = grupo
            self.descripcion = descripcion
            self.condicion_desbloqueo = condicion_desbloqueo
            self.sprite_idle = sprite_idle
            self.sprite_menu = sprite_menu
            self.posicion = posicion
        
        def esta_desbloqueado(self):
            """Verifica si el skin está desbloqueado."""
            if self.condicion_desbloqueo is None:
                return True  # Sin condición = siempre desbloqueado
            try:
                return self.condicion_desbloqueo()
            except:
                return False
    
    
    class SistemaSkins:
        """
        Gestor central del sistema de skins.
        Soporta grupos de skin por rutina y múltiples skins activos por NPC.
        """
        
        def __init__(self):
            self.skins = {}  # Todos los skins registrados {id: Skin}
        
        def registrar_skin(self, skin):
            """Registra un skin en el sistema."""
            self.skins[skin.id] = skin
        
        def obtener_skin(self, skin_id):
            """Obtiene un skin por su ID."""
            return self.skins.get(skin_id)
        
        def obtener_skins_npc(self, npc_id):
            """Obtiene todos los skins de un NPC."""
            return [s for s in self.skins.values() if s.npc_id == npc_id]
        
        def obtener_skins_desbloqueados(self, npc_id):
            """Obtiene los skins desbloqueados de un NPC."""
            return [s for s in self.obtener_skins_npc(npc_id) if s.esta_desbloqueado()]
        
        def obtener_grupos_npc(self, npc_id):
            """Obtiene los grupos únicos de skins de un NPC."""
            skins = self.obtener_skins_npc(npc_id)
            grupos = list(set(s.grupo for s in skins))
            # Ordenar para que "base" siempre esté primero
            grupos.sort(key=lambda g: (0 if g == "base" else 1, g))
            return grupos
        
        def obtener_grupos_con_skins(self, npc_id):
            """
            Obtiene los grupos donde el NPC tiene al menos 1 skin desbloqueado.
            Usado para filtrar el menú de skins.
            """
            skins_desbloqueados = self.obtener_skins_desbloqueados(npc_id)
            grupos = list(set(s.grupo for s in skins_desbloqueados))
            grupos.sort(key=lambda g: (0 if g == "base" else 1, g))
            return grupos
        
        def obtener_skins_grupo(self, npc_id, grupo):
            """Obtiene los skins de un NPC en un grupo específico."""
            return [s for s in self.obtener_skins_npc(npc_id) if s.grupo == grupo]
        
        def obtener_skins_desbloqueados_grupo(self, npc_id, grupo):
            """Obtiene los skins desbloqueados de un NPC en un grupo."""
            return [s for s in self.obtener_skins_grupo(npc_id, grupo) if s.esta_desbloqueado()]
        
        def obtener_skin_activo_grupo(self, npc_id, grupo):
            """Obtiene el skin activo de un NPC en un grupo específico."""
            skins_npc = store.skins_activos.get(npc_id, {})
            if isinstance(skins_npc, dict):
                skin_id = skins_npc.get(grupo)
                if skin_id:
                    skin = self.obtener_skin(skin_id)
                    if skin and skin.esta_desbloqueado():
                        return skin
            
            # Fallback: primer skin desbloqueado del grupo
            skins_disponibles = self.obtener_skins_desbloqueados_grupo(npc_id, grupo)
            if skins_disponibles:
                return skins_disponibles[0]
            
            return None
        
        def obtener_skin_activo(self, npc_id, grupo=None):
            """
            Obtiene el skin activo de un NPC.
            Si no se especifica grupo, usa el grupo de la rutina actual.
            """
            if grupo is None:
                grupo = obtener_grupo_rutina_actual(npc_id)
            return self.obtener_skin_activo_grupo(npc_id, grupo)
        
        def activar_skin(self, npc_id, skin_id):
            """Activa un skin para un NPC en su grupo correspondiente."""
            skin = self.obtener_skin(skin_id)
            if skin and skin.npc_id == npc_id and skin.esta_desbloqueado():
                # Asegurar estructura de dict
                if npc_id not in store.skins_activos:
                    store.skins_activos[npc_id] = {}
                elif not isinstance(store.skins_activos[npc_id], dict):
                    # Migrar formato antiguo
                    store.skins_activos[npc_id] = {}
                
                store.skins_activos[npc_id][skin.grupo] = skin_id

                return True
            return False
        
        def desactivar_skin_grupo(self, npc_id, grupo):
            """Desactiva el skin de un NPC en un grupo específico."""
            if npc_id in store.skins_activos and isinstance(store.skins_activos[npc_id], dict):
                if grupo in store.skins_activos[npc_id]:
                    del store.skins_activos[npc_id][grupo]
                    return True
            return False
        
        def desactivar_skin(self, npc_id):
            """Desactiva todos los skins de un NPC (vuelve al base)."""
            if npc_id in store.skins_activos:
                del store.skins_activos[npc_id]
                return True
            return False
        
        def hay_skins_disponibles(self, npc_id):
            """Verifica si hay skins registrados para un NPC (aunque no estén desbloqueados)."""
            return len(self.obtener_skins_npc(npc_id)) > 0
        
        def obtener_sprite_menu_por_grupo(self, npc_id, grupo):
            """
            Obtiene el sprite de menú del skin activo en un grupo específico.
            Con fallback a grupo base si no hay skin en el grupo.
            """
            skin = self.obtener_skin_activo_grupo(npc_id, grupo)
            if skin and skin.sprite_menu:
                return skin.sprite_menu
            
            # Fallback al grupo base si no hay skin en este grupo
            if grupo != "base":
                skin_base = self.obtener_skin_activo_grupo(npc_id, "base")
                if skin_base and skin_base.sprite_menu:
                    return skin_base.sprite_menu
            
            return None
        
        def obtener_sprite_idle_por_grupo(self, npc_id, grupo):
            """
            Obtiene el sprite idle del skin activo en un grupo específico.
            Con fallback a grupo base si no hay skin en el grupo.
            """
            skin = self.obtener_skin_activo_grupo(npc_id, grupo)
            if skin and skin.sprite_idle:
                return skin.sprite_idle
            
            # Fallback al grupo base si no hay skin en este grupo
            if grupo != "base":
                skin_base = self.obtener_skin_activo_grupo(npc_id, "base")
                if skin_base and skin_base.sprite_idle:
                    return skin_base.sprite_idle
            
            return None


# Instancia global del sistema de skins
define sistema_skins = SistemaSkins()

# Variable guardable para skins activos
# Formato: {npc_id: {grupo: skin_id}}
default skins_activos = {}


################################################################################
## Funciones de Grupos de Rutina
################################################################################

init python:
    
    def establecer_grupo_rutina(npc_id, dia, horario, grupo, condicion=None):
        """
        Asigna un grupo de skin a una rutina específica de un NPC.
        
        Args:
            npc_id: ID del NPC
            dia: Índice del día (0-6) o lista de días
            horario: Índice del horario (0-3)
            grupo: Grupo de skin a asignar
        """
        global rutinas_skin_grupos
        
        if npc_id not in rutinas_skin_grupos:
            rutinas_skin_grupos[npc_id] = {}
        
        entrada = {"grupo": grupo, "condicion": condicion} if condicion else grupo
        if isinstance(dia, (list, tuple)):
            for d in dia:
                rutinas_skin_grupos[npc_id][(d, horario)] = entrada
        else:
            rutinas_skin_grupos[npc_id][(dia, horario)] = entrada

    def obtener_grupo_rutina(npc_id, dia=None, horario=None):
        """
        Obtiene el grupo de skin asignado a una rutina específica.
        Si la entrada tiene condicion y ésta falla, retorna "base".
        """
        if dia is None:
            dia = getattr(store, 'dia_semana_actual', 0)
        if horario is None:
            horario = getattr(store, 'horario_actual', 0)

        grupos_npc = rutinas_skin_grupos.get(npc_id, {})
        entrada = grupos_npc.get((dia, horario), "base")

        if isinstance(entrada, dict):
            condicion = entrada.get("condicion")
            try:
                if condicion and not condicion():
                    return "base"
            except:
                return "base"
            return entrada.get("grupo", "base")
        return entrada
    
    def obtener_grupo_rutina_actual(npc_id):
        """
        Obtiene el grupo de skin de la rutina actual de un NPC.
        Wrapper conveniente para obtener_grupo_rutina.
        """
        return obtener_grupo_rutina(npc_id)


################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def registrar_skin(skin):
        """Registra un skin en el sistema."""
        sistema_skins.registrar_skin(skin)
    
    def obtener_skin_activo(npc_id, grupo=None):
        """Obtiene el skin activo de un NPC (por grupo o grupo actual)."""
        return sistema_skins.obtener_skin_activo(npc_id, grupo)
    
    def hay_skins_disponibles(npc_id):
        """Verifica si hay skins para un NPC."""
        return sistema_skins.hay_skins_disponibles(npc_id)
    
    def activar_skin(npc_id, skin_id):
        """Activa un skin para un NPC."""
        return sistema_skins.activar_skin(npc_id, skin_id)
    
    def desactivar_skin(npc_id, grupo=None):
        """Desactiva el skin de un NPC."""
        if grupo:
            return sistema_skins.desactivar_skin_grupo(npc_id, grupo)
        return sistema_skins.desactivar_skin(npc_id)
    
    def obtener_skins_desbloqueados(npc_id, grupo=None):
        """Obtiene la lista de skins desbloqueados de un NPC."""
        if grupo:
            return sistema_skins.obtener_skins_desbloqueados_grupo(npc_id, grupo)
        return sistema_skins.obtener_skins_desbloqueados(npc_id)
    
    def obtener_grupos_skins(npc_id):
        """Obtiene los grupos de skins de un NPC."""
        return sistema_skins.obtener_grupos_npc(npc_id)
    
    def obtener_grupos_con_skins(npc_id):
        """Obtiene los grupos donde el NPC tiene al menos 1 skin desbloqueado."""
        return sistema_skins.obtener_grupos_con_skins(npc_id)
    
    def obtener_sprite_menu_npc(npc_id):
        """
        Obtiene el sprite de menú actual del NPC.
        Basado en el grupo de la rutina actual.
        """
        grupo_actual = obtener_grupo_rutina_actual(npc_id)
        return sistema_skins.obtener_sprite_menu_por_grupo(npc_id, grupo_actual)
    
    def obtener_sprite_idle_rutina(npc_id):
        """
        Obtiene el sprite idle del NPC para la rutina actual.
        Basado en el grupo de la rutina actual.
        """
        grupo_actual = obtener_grupo_rutina_actual(npc_id)
        return sistema_skins.obtener_sprite_idle_por_grupo(npc_id, grupo_actual)

    # Mapeo de grupo de skin → prefijo del atributo de cuerpo en la layered image.
    # Actualizar aquí cuando se agregue un grupo con body propio.
    GRUPO_CUERPO_MAP = {
        "base":          "c_rbase",
        "pijama":        "c_pijama",
        "entrenamiento": "c_rbase",
        "bikini":        "c_rbase",
        "ropa_interior": "c_rbase",
        "vestidos":      "c_rbase",
    }

    def cuerpo_activo(npc_id):
        """
        Retorna el prefijo del atributo de cuerpo según el grupo de skin activo del NPC.
        Usar para evaluar qué skin mostrar al inicio de una quest.

        Returns:
            str: "c_rbase" o "c_pijama" según el grupo activo.
        """
        grupo = obtener_grupo_rutina_actual(npc_id)
        return GRUPO_CUERPO_MAP.get(grupo, "c_rbase")
