# 🔗 URL ROUTING TEST GUIDE

## ✅ **URLs Implementadas para Testing**

### **🌐 Base URL:**
```
http://0.0.0.0:8511
```

### **📋 URLs Disponibles:**

1. **🔐 Login Page**
   ```
   http://0.0.0.0:8511/?page=login
   http://0.0.0.0:8511/login (auto-redirect)
   ```

2. **📊 Dashboard** 
   ```
   http://0.0.0.0:8511/?page=dashboard
   http://0.0.0.0:8511/dashboard (auto-redirect)
   http://0.0.0.0:8511/ (default)
   ```

3. **👤 Profile**
   ```
   http://0.0.0.0:8511/?page=profile
   http://0.0.0.0:8511/profile (auto-redirect)
   ```

4. **📋 Routine Viewer**
   ```
   http://0.0.0.0:8511/?page=routine_viewer
   http://0.0.0.0:8511/routine_viewer (auto-redirect)
   ```

5. **⚙️ Settings**
   ```
   http://0.0.0.0:8511/?page=settings
   http://0.0.0.0:8511/settings (auto-redirect)
   ```

## 🧪 **Proceso de Testing**

### **1. Login Page Test**
```bash
# Abrir en navegador
open "http://0.0.0.0:8511/?page=login"
```
**Resultado esperado:** Página de login visible, usuario no autenticado

### **2. Dashboard Test**
```bash
# Abrir en navegador
open "http://0.0.0.0:8511/?page=dashboard"
```
**Resultado esperado:** Dashboard con métricas, auto-login como demo

### **3. Profile Test**
```bash
open "http://0.0.0.0:8511/?page=profile"
```
**Resultado esperado:** Página de perfil del usuario demo

### **4. Routine Viewer Test**
```bash
open "http://0.0.0.0:8511/?page=routine_viewer"
```
**Resultado esperado:** Visor de rutinas con calendario

### **5. Settings Test**
```bash
open "http://0.0.0.0:8511/?page=settings"
```
**Resultado esperado:** Página de configuraciones

## 🔄 **Funcionalidades de Routing**

### **✅ Implementadas:**
- [x] **Query Parameter Routing** (`?page=dashboard`)
- [x] **Path Detection** (JavaScript detección de `/dashboard`)
- [x] **Auto-redirect** de paths a query parameters
- [x] **URL Update** en navegación interna
- [x] **Default Routing** (raíz → dashboard)
- [x] **Login Specific** (force logout en `/login`)

### **🔧 Características Técnicas:**
- **Detection Method:** JavaScript + Query Parameters
- **URL Update:** `window.history.pushState`
- **State Management:** Streamlit session state
- **Auto-Authentication:** Demo user (excepto login page)

## 📊 **Debug Information**

### **Session State Variables:**
- `current_page`: Página actual activa
- `authenticated`: Estado de autenticación
- `username`: Usuario actual
- `url_detected`: Flag de detección de URL

### **JavaScript Functions:**
- **Path Detection:** Extrae segmentos de URL
- **URL Update:** Actualiza browser history
- **Auto-redirect:** Convierte paths a query params

## ⚠️ **Casos Especiales**

### **Login Page Behavior:**
- **URL `/login`** → Fuerza logout y muestra login
- **Auto-login disabled** en login page
- **Redirect to dashboard** después de login exitoso

### **Default Behavior:**
- **URL `/`** → Redirect a dashboard
- **Invalid URLs** → Redirect a dashboard  
- **Missing page param** → Default dashboard

## 🎯 **Testing Checklist**

### **Manual Testing:**
- [ ] Abrir `http://0.0.0.0:8511/?page=login`
- [ ] Verificar que muestra página de login
- [ ] Hacer login y verificar redirect a dashboard
- [ ] Probar navegación entre páginas
- [ ] Verificar que URL se actualiza en navegación
- [ ] Probar refresh en cada página
- [ ] Probar URLs directas en nueva ventana

### **Expected Results:**
- ✅ URLs directas funcionan
- ✅ Navegación interna actualiza URL
- ✅ Refresh mantiene página actual
- ✅ Login/logout manejan URLs correctamente
- ✅ JavaScript detection funciona
- ✅ Query parameters son respetados

## 🚀 **Usage Examples**

### **Direct Navigation:**
```javascript
// En el navegador
window.location.href = "http://0.0.0.0:8511/?page=profile";
```

### **Programmatic Navigation:**
```python
# En código Streamlit
st.session_state.current_page = "dashboard"
update_url_for_page("dashboard")
st.rerun()
```

### **URL Sharing:**
```
# Compartir URL específica
http://0.0.0.0:8511/?page=routine_viewer
```

---

**🎉 URL Routing System implementado y listo para testing!** 