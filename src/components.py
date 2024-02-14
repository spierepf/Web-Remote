class Components:
    def button(self, label, icon, action):
        return f"""<div class="d-flex flex-column align-items-center" onclick="{action}">""" \
               + f"""<i class="{icon}"></i>""" \
               + f"""<span class="label">{label}</span>""" \
               + f"""</div>"""

    def scroll(self, label, up_icon, up_action, dn_icon, dn_action):
        return f"""<div class="d-flex flex-column rounded-bg py-3 px-4 justify-content-center align-items-center">""" \
               + f"""<i class="{up_icon}" onclick="{up_action}"></i>""" \
               + f"""<span class="label py-3">{label}</span>""" \
               + f"""<i class="{dn_icon}" onclick="{dn_action}"></i>""" \
               + f"""</div>"""
