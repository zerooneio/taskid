from app import app, mysql
from flask import render_template, url_for, redirect, request, session, flash

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connection.cursor()
    ss = conn.execute("SELECT reg_periksa.no_rawat, reg_periksa.no_rkm_medis, pasien.nm_pasien, poliklinik.nm_poli, referensi_mobilejkn_bpjs_taskid.taskid FROM reg_periksa INNER JOIN pasien INNER JOIN poliklinik INNER JOIN referensi_mobilejkn_bpjs_taskid ON reg_periksa.no_rkm_medis=pasien.no_rkm_medis AND reg_periksa.kd_poli=poliklinik.kd_poli AND reg_periksa.no_rawat=referensi_mobilejkn_bpjs_taskid.no_rawat WHERE reg_periksa.tgl_registrasi=CURRENT_DATE() ORDER BY reg_periksa.no_rawat ASC")
    rs = conn.fetchall()
    task_3 = 0
    task_4 = 0
    task_5 = 0
    task_6 = 0
    task_7 = 0
    task_99 = 0
    for row in rs :
        task_3 += row[4] == '3'
        task_4 += row[4] == '4'
        task_5 += row[4] == '5'
        task_6 += row[4] == '6'
        task_7 += row[4] == '7'
        task_99 += row[4] == '99'
    return render_template('taskid_now.html', rs=rs, ss=ss, task_3=task_3, task_4=task_4, task_5=task_5, task_6=task_6, task_7=task_7, task_99=task_99)

@app.route('/poli', methods=['GET', 'POST'])
def task_poli():
    conn = mysql.connection.cursor()
    conn.execute("SELECT kd_poli, nm_poli FROM `poliklinik` WHERE status='1'")
    rs_pol = conn.fetchall()
    conn.close()
    if request.method == 'POST' :
        pol = request.form['pol']

        conn = mysql.connection.cursor()
        ss = conn.execute(f"SELECT reg_periksa.no_rawat, reg_periksa.no_rkm_medis, pasien.nm_pasien, poliklinik.nm_poli, referensi_mobilejkn_bpjs_taskid.taskid FROM reg_periksa INNER JOIN pasien INNER JOIN poliklinik INNER JOIN referensi_mobilejkn_bpjs_taskid ON reg_periksa.no_rkm_medis=pasien.no_rkm_medis AND reg_periksa.kd_poli=poliklinik.kd_poli AND reg_periksa.no_rawat=referensi_mobilejkn_bpjs_taskid.no_rawat WHERE reg_periksa.tgl_registrasi=CURRENT_DATE()  AND reg_periksa.kd_poli='{pol}' ORDER BY reg_periksa.no_rawat ASC")
        rs = conn.fetchall()
        conn.execute("SELECT kd_poli, nm_poli FROM `poliklinik` WHERE status='1'")
        rs_pol = conn.fetchall()
        conn.execute(f"SELECT nm_poli FROM `poliklinik` WHERE status='1' AND kd_poli='{pol}'")
        nm_pol = conn.fetchone()[0]
        
        conn.close()
        task_3 = 0
        task_4 = 0
        task_5 = 0
        task_6 = 0
        task_7 = 0
        task_99 = 0
        for row in rs :
            task_3 += row[4] == '3'
            task_4 += row[4] == '4'
            task_5 += row[4] == '5'
            task_6 += row[4] == '6'
            task_7 += row[4] == '7'
            task_99 += row[4] == '99'
        print(nm_pol)
        return render_template('taskid_poli.html', rs=rs, rs_pol=rs_pol, nm_pol=nm_pol, ss=ss, task_3=task_3, task_4=task_4, task_5=task_5, task_6=task_6, task_7=task_7, task_99=task_99)
    return render_template('taskid_poli.html', rs_pol=rs_pol)