import sys
import re

def parse_md():
    with open(r"c:\Users\farha\OneDrive\Desktop\inssinglepage\notes data.md", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    titles = [
        ("db-security", "Database Security.*Concept Notes"),
        ("tls", "Transport Layer Security \(TLS\).*Concept Notes"),
        ("ipsec", "IP Security \(IPSec\).*Concept Notes"),
        ("ids", "Intrusion Detection Systems \(IDS\).*Concept Notes"),
        ("firewall-vpn", "Firewall & VPN.*Study Notes"),
        ("auth-vuln", "Authentication & Its Vulnerabilities.*Study Notes"),
        ("kerberos", "User Authentication & Kerberos.*Study Notes"),
        ("msg-auth", "Message Authentication.*Notes"),
        ("digital-sig", "Digital Signatures.*Notes"),
        ("cloud-threats", "Cloud Computing & Common Cyber Threats.*Notes"),
        ("key-exchange", "Key Exchange & MAC vs MDC.*Quick Notes")
    ]
    
    indices = []
    # Try to find each title using regex because of encoding issues with dashes
    for _id, pattern in titles:
        match = re.search(pattern, content)
        if match:
            indices.append((match.start(), _id, pattern))
        else:
            print(f"NOT FOUND: {pattern}")
            
    indices.sort(key=lambda x: x[0])
    
    sections = []
    for i in range(len(indices)):
        start = indices[i][0]
        end = indices[i+1][0] if i + 1 < len(indices) else len(content)
        sections.append((indices[i][1], indices[i][2], content[start:end].strip()))
        
    with open(r"c:\Users\farha\OneDrive\Desktop\inssinglepage\inssinglepage.html", "r", encoding="utf-8") as f:
        html = f.read()
        
    titles_display = {
        "db-security": ("Database Security", "Concept Notes"),
        "tls": ("Transport Layer Security (TLS)", "Concept Notes"),
        "ipsec": ("IP Security (IPSec)", "Concept Notes"),
        "ids": ("Intrusion Detection Systems (IDS)", "Concept Notes"),
        "firewall-vpn": ("Firewall & VPN", "Study Notes"),
        "auth-vuln": ("Authentication & Its Vulnerabilities", "Study Notes"),
        "kerberos": ("User Authentication & Kerberos", "Study Notes"),
        "msg-auth": ("Message Authentication", "Notes"),
        "digital-sig": ("Digital Signatures", "Notes"),
        "cloud-threats": ("Cloud Computing & Common Cyber Threats", "Notes"),
        "key-exchange": ("Key Exchange & MAC vs MDC", "Quick Notes")
    }
    
    topic_keys = [t[0] for t in titles]

    TOPIC_FILES = {
        "db-security": ("file Database Security.pdf", "pdf"),
        "tls": ("file TLS-SSL.ppt", "ppt"),
        "ipsec": ("file Security.pptx", "pptx"),
        "ids": ("file IDS.pptx", "pptx"),
        "firewall-vpn": ("file Firewall & VPN (1).pptx", "pptx"),
        "auth-vuln": ("file Authentication ans its Vulnerabilities.pptx", "pptx"),
        "kerberos": ("file User Authentication.pdf", "pdf"),
        "msg-auth": ("file Message Authentication.ppt", "ppt"),
        "digital-sig": ("file Digital Signature.ppt", "ppt"),
        "cloud-threats": ("file cloud and cyberthreats.pdf", "pdf")
    }

    def format_content(_id, text):
        lines = text.split('\n')
        out = []
        
        main_title, sub_title = titles_display[_id]
        file_no = f"FILE {str(topic_keys.index(_id) + 1).zfill(2)}"
        
        out.append('<div class="topic-head">')
        out.append('  <div class="topic-eyebrow">')
        out.append(f'    <span class="file-no">{file_no}</span>')
        out.append('    <span class="deck-tag">INFOSEC DOSSIER</span>')
        out.append('  </div>')
        out.append(f'  <h2 class="topic-title">{main_title}</h2>')
        out.append(f'  <div class="topic-brief">{sub_title}</div>')
        if _id in TOPIC_FILES:
            fname, ftype = TOPIC_FILES[_id]
            out.append('  <div class="file-attachment">')
            out.append(f'    <span class="file-type-badge {ftype}">{ftype.upper()}</span>')
            out.append(f'    <a href="{fname}" target="_blank" class="file-link">')
            out.append('      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>')
            out.append(f'      {fname}')
            out.append('    </a>')
            out.append('  </div>')
        out.append('</div>')
        
        content_lines = lines[1:]
        if content_lines and ('____' in content_lines[0] or 'Week' in content_lines[0] or 'Information Security' in content_lines[0]):
            content_lines = content_lines[1:]
        if content_lines and ('____' in content_lines[0] or 'Week' in content_lines[0] or 'Information Security' in content_lines[0]):
            content_lines = content_lines[1:]
            
        in_list = False
        in_table = False
        in_qa = False
        
        for line in content_lines:
            line = line.strip()
            if not line or line.startswith('____'):
                continue
                
            if 'Quick Reference' in line or 'Cheat Sheet' in line:
                if in_table:
                    out.append('</table>')
                    in_table = False
                if in_list:
                    out.append('</ul>')
                    in_list = False
                out.append('<div class="cheat">')
                out.append('<div class="cheat-head"><h5>Quick Reference Cheat Sheet</h5><span class="stamp-text">EXAM PREP</span></div>')
                out.append('<div class="qa-grid">')
                in_qa = True
                continue
                
            if in_qa:
                if line.startswith('Q:'):
                    if '?' in line:
                        q_part, a_part = line[2:].split('?', 1)
                        q_part = q_part.strip() + "?"
                    else:
                        q_part = line[2:]
                        a_part = ""
                    a_part = a_part.strip()
                    if not a_part:
                        out.append(f'<div class="qa-card"><div class="q">{q_part}</div><div class="a"></div></div>')
                    else:
                        out.append(f'<div class="qa-card"><div class="q">{q_part}</div><div class="a">{a_part}</div></div>')
                else:
                    # Append to previous answer if possible, otherwise it's just text
                    if out and out[-1].endswith('</div></div>'):
                        out[-1] = out[-1][:-14] + " " + line + '</div></div>'
                    else:
                        out.append(f'<div class="qa-card"><div class="a">{line}</div></div>')
                continue
                
            m3 = re.match(r'^(\d+)\.\s+(.*)', line)
            if m3:
                if in_table: out.append('</table>'); in_table = False
                if in_list: out.append('</ul>'); in_list = False
                out.append(f'<h3><span class="num">{m3.group(1)}.</span> {m3.group(2)}</h3>')
                continue
                
            m4 = re.match(r'^([A-Z])\)\s+(.*)', line)
            if m4:
                if in_table: out.append('</table>'); in_table = False
                if in_list: out.append('</ul>'); in_list = False
                out.append(f'<h4>{m4.group(1)}) {m4.group(2)}</h4>')
                continue
                
            if line.startswith(' ') or line.startswith('- '):
                if in_table: out.append('</table>'); in_table = False
                if not in_list:
                    out.append('<ul>')
                    in_list = True
                out.append(f'<li>{line[2:].strip()}</li>')
                continue
            else:
                if in_list:
                    out.append('</ul>')
                    in_list = False
                    
            if '\t' in line:
                if in_list: out.append('</ul>'); in_list = False
                parts = line.split('\t')
                if len(parts) > 1:
                    if not in_table:
                        out.append('<table class="data">')
                        out.append('<tr>' + ''.join(f'<th>{p}</th>' for p in parts) + '</tr>')
                        in_table = True
                    else:
                        out.append('<tr>' + ''.join(f'<td>{p}</td>' for p in parts) + '</tr>')
                    continue
            
            if in_table:
                out.append('</table>')
                in_table = False
                
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            out.append(f'<p>{line}</p>')
            
        if in_list:
            out.append('</ul>')
        if in_table:
            out.append('</table>')
        if in_qa:
            out.append('</div></div>')
            
        out.append(f'''
<div class="mcq-zone" data-topic="{_id}" id="mcq-zone-{_id}"></div>
<div class="exhibit">
  <div class="corner-bl"></div><div class="corner-br"></div>
  <div class="exhibit-label">
    <span>DIAGRAM SPACE</span>
  </div>
  <div class="exhibit-zone has-image" data-topic="{_id}">
    <img src="temp.img" alt="Diagram">
  </div>
  <div class="exhibit-actions" style="display:flex;">
    <button class="exhibit-replace">Replace</button>
    <button class="exhibit-remove danger">Remove</button>
  </div>
  <input type="file" class="exhibit-file" accept="image/*" style="display:none;">
</div>
<div class="topic-footer">
  <button class="nav-btn prev" data-nav="prev"><span class="nb-label">PREV CASE</span><span class="nb-title">--</span></button>
  <button class="nav-btn next" data-nav="next"><span class="nb-label">NEXT CASE</span><span class="nb-title">--</span></button>
</div>
<label class="mark-reviewed">
  <input type="checkbox" class="reviewed-checkbox" data-topic="{_id}">
  I have mastered this case file
</label>
        ''')
        
        return '\n'.join(out)

    for _id, title, text in sections:
        html_content = format_content(_id, text)
        marker = f"<!-- CONTENT:{_id} -->"
        if marker in html:
            html = html.replace(marker, html_content)
        else:
            print(f"Marker {marker} not found!")
            
    with open(r"c:\Users\farha\OneDrive\Desktop\inssinglepage\inssinglepage.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Done generating HTML!")

if __name__ == "__main__":
    parse_md()
