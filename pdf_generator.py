from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime

def generate_report(filename,name,career,confidence,description,salary,skills,courses,top3):
    styles=getSampleStyleSheet()
    title=styles["Title"]; title.alignment=TA_CENTER
    heading=styles["Heading2"]; heading.textColor=colors.HexColor("#2563eb")
    normal=styles["BodyText"]

    pdf=SimpleDocTemplate(filename,leftMargin=35,rightMargin=35,topMargin=35,bottomMargin=35)
    story=[]

    story.append(Paragraph("<font color='#2563eb' size='26'><b>Career Twin AI</b></font>",title))
    story.append(Paragraph("<font color='#64748b'>AI Powered Career Recommendation Report</font>",styles["Normal"]))
    story.append(Spacer(1,10))

    line=Table([[""]],colWidths=[520])
    line.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#2563eb"))]))
    story.append(line); story.append(Spacer(1,12))

    today=datetime.now().strftime("%d %B %Y %I:%M %p")

    info=Table([
        ["Student Name",name],
        ["Generated On",today],
        ["Recommended Career",career],
        ["Confidence Score",f"{confidence}%"]
    ],colWidths=[180,340])

    info.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#2563eb")),
        ("TEXTCOLOR",(0,0),(0,-1),colors.white),
        ("BACKGROUND",(1,0),(1,-1),colors.HexColor("#eef4ff")),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#cbd5e1")),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10)
    ]))
    story.append(info); story.append(Spacer(1,14))

    story.append(Paragraph("<b>Career Match Score</b>",heading))
    pct=max(0,min(float(confidence),100))
    filled=int((pct/100)*40)
    bar="█"*filled+"░"*(40-filled)
    story.append(Paragraph(f"<font color='#2563eb'>{bar}</font> <b>{confidence}%</b>",normal))
    story.append(Spacer(1,14))

    story.append(Paragraph("<b>Top 3 AI Recommendations</b>",heading))
    data=[["Rank","Career","Confidence"]]
    medals=["🥇","🥈","🥉"]
    for i,item in enumerate(top3):
        data.append([medals[i],item["career"],f"{item['score']}%"])
    t=Table(data,colWidths=[60,300,120])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563eb")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#eef4ff")]),
        ("GRID",(0,0),(-1,-1),0.4,colors.grey),
        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ]))
    story.append(t); story.append(Spacer(1,12))

    story.append(Paragraph("<b>Career Description</b>",heading))
    story.append(Paragraph(description,normal)); story.append(Spacer(1,10))

    story.append(Paragraph("<b>Required Skills</b>",heading))
    for s in skills: story.append(Paragraph("✔ "+s,normal))
    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Recommended Courses</b>",heading))
    for c in courses: story.append(Paragraph("📘 "+c,normal))
    story.append(Spacer(1,10))

    sal=Table([["Average Salary",salary]],colWidths=[200,320])
    sal.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),colors.HexColor("#16a34a")),
        ("TEXTCOLOR",(0,0),(0,0),colors.white),
        ("BACKGROUND",(1,0),(1,0),colors.HexColor("#dcfce7")),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey)
    ]))
    story.append(sal); story.append(Spacer(1,18))

    story.append(Paragraph("<font color='#2563eb'><b>Career Twin AI</b></font>",heading))
    story.append(Paragraph("This report was generated using Artificial Intelligence and Machine Learning.",normal))
    story.append(Paragraph("<font color='#64748b'>© 2026 Career Twin AI</font>",styles["Normal"]))
    pdf.build(story)
    return filename
