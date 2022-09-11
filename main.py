import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
# NEW LIBRARIES FOR BUILDOZER
import requests
import bcrypt
import datetime
############################

def clock_now():
	clock_now = datetime.datetime.utcnow()+datetime.timedelta(hours=3)
	clock_now_return = clock_now.strftime("%d-%m-%Y %H:%M:%S")
	return clock_now_return

forms_number_id = 0
log_out_id = 0
idx_command = 0

class Pag1(Screen):
	def on_pre_enter(self,*args):
		Clock.schedule_once(self.cookie_login, 1) # TIMER

	def cookie_login(self, *args):
		global log_out_id
		if log_out_id == 0:
			conn = sqlite3.connect("modulo_app.db")

			# Create a Cursor
			c = conn.cursor()


			c.execute("SELECT * FROM login_user_cookie")

			
			# Verification step
			verification_step = c.fetchone()

			if verification_step[0] != 'None':
				self.ids.user.text = verification_step[0]
				self.ids.user.helper_text = "User ID"
				self.ids.user.helper_text_mode = "on_focus"
			elif verification_step[0] == 'None':
				self.ids.user.hint_text = "User    "
				self.ids.user.mode =  "rectangle"
			conn.close()



	def submit(self, *args):
		try:
			global forms_number_id

			conn = sqlite3.connect("modulo_app.db")

			# Create a Cursor
			c = conn.cursor()
			# PENTRU USER SIMPLI --------------------------------------------------------------------------------------------------VERIFICARE


			if self.ids.user.text != '' and self.ids.password.text != '':

				c.execute("SELECT * FROM users WHERE user=:user", {"user": self.ids.user.text})
				# Verification step
				verification_step = c.fetchone()
		
				if verification_step[0] == self.ids.user.text and bcrypt.checkpw(bytes(self.ids.password.text,'utf-8'), bytes(verification_step[1],'utf-8')) and verification_step[2] != None:
					split_name = verification_step[0].split("@")
					self.ids.welcome_label.font_size = '25dp'
					self.ids.welcome_label.text = f"[color=#0d6efd]Wel[/color][color=FFFFFF]come[/color] {split_name[0].capitalize()}!"
					#----NUMBERS FORM
					c.execute("SELECT * FROM login_user_cookie")
					verification_step = c.fetchone()
					#----NUMBERS FORM
					if self.ids.user.text == verification_step[0]:
						forms_number_id = int(verification_step[1])

					else:
						forms_number_id = 0
						c.execute("UPDATE login_user_cookie SET user =?, sent_forms =?", (self.ids.user.text, '0'))
						conn.commit()
						conn.close()
					Clock.schedule_once(self.next_screen, 2) # TIMER

 
				else:
					self.ids.welcome_label.font_size = '20dp'
					self.ids.welcome_label.text = "[color=ff0000]Wrong[/color] Password!"
					conn.close()
			else:
				self.ids.welcome_label.font_size = '20dp'
				self.ids.welcome_label.text = "[color=ff0000]Wrong[/color] User or Password"


				# conn.commit()
				conn.close()

		# EROARE USERNAME DIN DATABASE --------------------------------------------------------------------------------------------------VERIFICARE
		except Exception as e:
			self.ids.welcome_label.font_size = '20sp'
			self.ids.welcome_label.text = "[color=ff0000]Wrong[/color] Username!"
			conn.close()

	# DELAY TRANSITIE PAGINA LOGIN--------------------------------------------------------------------------------------------------DELAY
	def next_screen(self, *args): # asta e pentru delay-ul acela pentru pagina de inceput
		global log_out_id
		self.manager.current = 'pag2'
		self.manager.transition.direction="left"		
		log_out_id = 0
	def on_checkbox_active(self, checkbox, value):
		if value:
			self.ids.password.password = False
			self.ids.password.icon_right = "eye"
		else:
			self.ids.password.password = True
			self.ids.password.icon_right = "eye-off"

class Pag2(Screen):
	def on_pre_enter(self, *args):
		try:
			self.ids.refresh_id_page0.icon = 'images/delivered.png'
			Clock.schedule_interval(self.try_and_connect_api, 10)
			#TITLE STYLE
			self.ids.mdtool.ids.label_title.font_name = "data/font/Bungee-Regular.ttf"
			self.ids.mdtool.ids.label_title.font_size = "15sp"
			#-----------

			user_id = self.manager.get_screen("pag1").ids.user.text # THIS IS HOW YOU TAKE INFOS FROM ANOTHER CLASSS!!!!!!!!!
			self.ids.profil_id_profilo.text = f"[color=#FFFFFF]{user_id.split('@')[0].capitalize()}[/color]"
			conn = sqlite3.connect("modulo_app.db")
			# Create a Cursor
			c = conn.cursor()
			#--------------------------------------------VERIFICARE
			c.execute("SELECT * FROM users WHERE user=:user", {"user": user_id})
			# Verification step
			verification_step = c.fetchone()

			if verification_step[2] == '3': # TORINO
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-3[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-3[/color]"
			elif verification_step[2] == '4': # VERONA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-4[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-4[/color]"
			elif verification_step[2] == '5': # GORGONZOLA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-5[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-5[/color]"
			elif verification_step[2] == '6': # VENEZIA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-6[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-6[/color]"
			elif verification_step[2] == '7': # RAVENA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-7[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-7[/color]"
			elif verification_step[2] == '8': # BOLOGNA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-8[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-8[/color]"
			elif verification_step[2] == '9': # RIMINI
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-9[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-9[/color]"
			elif verification_step[2] == '10': # PESCARA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-10[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-10[/color]"
			elif verification_step[2] == '11': # PRATO
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-11[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-11[/color]"
			elif verification_step[2] == '12': # PISA
				self.ids.mdtool.title = "[color=FFFFFF]Modulo Preposti[/color] - [color=#0d6efd]Depozit-12[/color]"
				self.ids.deposit_id_profilo.text = "[color=#0d6efd]Depozit-12[/color]"
			# conn.commit()
			conn.close()

		# EROARE DIN DATABASE --------------------------------------------------------------------------------------------------VERIFICARE
		except Exception as e:
			conn.close()




#LOGIC PART OF THE API AND FORM
	def api_request(self, *args):
		try:
			global forms_number_id
			user_id = self.manager.get_screen("pag1").ids.user.text # THIS IS HOW YOU TAKE INFOS FROM ANOTHER CLASSS!!!!!!!!!
			# self.update_form_number_cookie()
			conn = sqlite3.connect("modulo_app.db")
			# Create a Cursor
			c = conn.cursor()
			#--------------------------------------------VERIFICARE
			c.execute("UPDATE login_user_cookie SET sent_forms =?", (forms_number_id,))
			c.execute("SELECT * FROM users WHERE user=:user", {"user": user_id})
			# Verification step
			verification_step = c.fetchone()

			eq_id_api = self.ids.eq_id.text
			buono_id_api = self.ids.buono_id.text
			tipologia_id_api = self.ids.tipologia_id.text
			grafiiato_id_api = self.ids.graffiato_id.text
			intervento_id_api = self.ids.intervento_id.text
			note_id_api = self.ids.note_id.text
			

			if eq_id_api == '' or buono_id_api == '' or tipologia_id_api == 'Scegli [color=#0d6efd]Tipologia merce[/color]' or grafiiato_id_api == 'Scegli [color=#0d6efd]Graffiato/Rigato[/color]' or intervento_id_api == 'Select [color=#0d6efd]Intervento[/color]':
				self.ids.error_label_infos.opacity = 1
				self.ids.error_label_infos.text = "[color=#FFFFFF]Valori di[/color][color=ff0000] errore![/color]"
			else:
				if eq_id_api.isdigit() != True or len(eq_id_api) != 4:
					self.ids.error_label_infos.opacity = 1
					self.ids.error_label_infos.text = "[color=#FFFFFF]Valori di[/color][color=ff0000] errore!(Eq 4 numeri)[/color]"
				else:
					self.ids.error_label_infos.opacity = 0
					author_id_number = None

					if 'user10' in user_id or 'user11' in user_id or 'user12' in user_id or 'user13' in user_id or 'user14' in user_id or 'user15' in user_id or 'user16' in user_id or 'user17' in user_id or 'user18' in user_id or 'user19' in user_id or 'user20' in user_id:
						author_id_number = int(user_id.split('@')[0][10-2:])
					else:
						author_id_number = int(user_id.split('@')[0][-1])
					
					BASE ="http://127.0.0.1:5000/"
					response = requests.get(BASE + "example1/0/")
					last_id = response.json()

					self.connection_data_send_try()

					data_base = [
						{"eq":int(eq_id_api),"buono":buono_id_api, "tipologia_merce":tipologia_id_api,"graffiato":grafiiato_id_api,"intervento":intervento_id_api, "deposit":int(verification_step[2]),"author":int(author_id_number), "note": note_id_api}
					]

					for x in range(len(data_base)):
						# -----------------PUT
						forms_number_id += int(len(data_base))
						response = requests.put(BASE + f"example1/{last_id['id']+1}", data_base[0])
						response_dict = response.json()

						try:
							if 'Error' in response_dict['message']:
								self.ids.error_label_infos.text = '[color=ff0000]Errore[/color][color=#FFFFFF] di Database - vedi stato! Dati non trasmessi![/color]'
								self.ids.error_label_infos.opacity = 1
								self.ids.refresh_id_page3.opacity = 1
								self.ids.refresh_id_page3.disabled = False						
						except:
							pass




					#------------CLEAR FORMS
					self.ids.eq_id.text = ''
					self.ids.buono_id.text = ''
					self.ids.tipologia_id.text = 'Scegli [color=0d6efd]Tipologia merce[/color]'
					self.ids.graffiato_id.text = 'Scegli [color=0d6efd]Graffiato/Rigato[/color]'
					self.ids.intervento_id.text = 'Select [color=0d6efd]Intervento[/color]'
					self.ids.note_id.text = ''

			conn.commit()
			conn.close()

		except Exception as e:
			conn = sqlite3.connect("modulo_app.db")
			deposit = None

			if int(verification_step[2]) == 3:
				deposit = 'Depozit3'
			elif int(verification_step[2]) == 4:
				deposit = 'Depozit4'
			elif int(verification_step[2]) == 5:
				deposit = 'Depozit5'
			elif int(verification_step[2]) == 6:
				deposit = 'Depozit6'
			elif int(verification_step[2]) == 7:
				deposit = 'Depozit7'
			elif int(verification_step[2]) == 8:
				deposit = 'Depozit8'
			elif int(verification_step[2]) == 9:
				deposit = 'Depozit9'
			elif int(verification_step[2]) == 10:
				deposit = 'Depozit10'
			elif int(verification_step[2]) == 11:
				deposit = 'Depozit11'
			elif int(verification_step[2]) == 12:
				deposit = 'Depozit12'

			self.connection_data_send_except()
			# Create a Cursor
			c = conn.cursor()
			c.execute(f"INSERT INTO {deposit} VALUES (:eq, :buono, :tipologia_merce, :graffiato, :intervento, :deposit, :author, :note)", {"eq":int(eq_id_api),"buono":buono_id_api, "tipologia_merce":tipologia_id_api,"graffiato":grafiiato_id_api,"intervento":intervento_id_api, "deposit":int(verification_step[2]),"author":int(author_id_number), "note": note_id_api})
			conn.commit()
			conn.close()

			#------------CLEAR FORMS
			self.ids.eq_id.text = ''
			self.ids.buono_id.text = ''
			self.ids.tipologia_id.text = 'Scegli [color=#0d6efd]Tipologia merce[/color]'
			self.ids.graffiato_id.text = 'Scegli [color=#0d6efd]Graffiato/Rigato[/color]'
			self.ids.intervento_id.text = 'Select [color=#0d6efd]Intervento[/color]'
			self.ids.note_id.text = ''






	def try_and_connect_api(self, *args):
		try:
			global forms_number_id
			# self.update_form_number_cookie()
			user_id = self.manager.get_screen("pag1").ids.user.text # THIS IS HOW YOU TAKE INFOS FROM ANOTHER CLASSS!!!!!!!!!
			conn = sqlite3.connect("modulo_app.db")
			# Create a Cursor
			c = conn.cursor()
			#--------------------------------------------VERIFICARE
			c.execute("UPDATE login_user_cookie SET sent_forms =?", (forms_number_id,))
			c.execute("SELECT * FROM users WHERE user=:user", {"user": user_id})
			# Verification step
			verification_step_user = c.fetchone()
			#--------------------------------------------VERIFICARE
			c.execute(f"SELECT * FROM {verification_step_user[3]}")
			# Verification step
			verification_step = c.fetchall()




			if verification_step == []:
				self.ids.forms_number_profilo.text = f"Moduli non inviati: 0"
			

			else:

				for num_x in verification_step:
					BASE ="http://127.0.0.1:5000/"
					response = requests.get(BASE + "example1/0/")
					last_id = response.json()

					data_base = [
					{"eq":int(num_x[0]),"buono":num_x[1], "tipologia_merce":num_x[2],"graffiato":num_x[3],"intervento":num_x[4], "deposit":int(num_x[5]),"author":int(num_x[6]), "note": num_x[7]}
					]
					# -----------------PUT
					response = requests.put(BASE + f"example1/{last_id['id']+1}", data_base[0])
					response_dict = response.json()
					self.connection_data_send_try()
					self.ids.forms_number_profilo.text = f"Moduli non inviati: 0"


					try:
						if 'Error' in response_dict['message']:
							self.ids.error_label_infos.text = '[color=ff0000]Errore[/color][color=#0d6efd] di Database - vedi stato! Dati non trasmessi![/color]'
							self.ids.error_label_infos.opacity = 1
							self.ids.refresh_id_page3.opacity = 1
							self.ids.refresh_id_page3.disabled = False						
					except:
						pass

					forms_number_id += int(len(data_base))

				c.execute(f"DELETE FROM {verification_step_user[3]}")


			c.execute("SELECT * FROM login_user_cookie")
			# Verification step
			verification_step_user = c.fetchone()
			self.ids.forms_number_delivered_profilo.text = f"Moduli inviati: {verification_step_user[1]}"

			conn.commit()
			conn.close()

		except Exception as e:
			c.execute("SELECT * FROM login_user_cookie")
			# Verification step
			verification_step_user = c.fetchone()
			self.ids.forms_number_delivered_profilo.text = f"Moduli inviati: {verification_step_user[1]}"
			self.ids.forms_number_profilo.text = f"Moduli non inviati: {len(verification_step)}"
			self.connection_data_send_except()
			conn.close()




	def connection_data_send_except(self,*args):
		try:
			self.ids.refresh_id_page0.icon = 'images/undelivered.png'
			self.ids.refresh_id_page.icon = 'close'
			self.ids.refresh_id_page2.icon = 'wifi-off'
			self.ids.infos_status.text = '[color=ff0000]Non è stato possibile[/color][color=#0d6efd] inviare i dati![/color]'
		except:
			pass
	def connection_data_send_try(self,*args):
		try:
			self.ids.refresh_id_page0.icon = 'images/delivered.png'
			self.ids.refresh_id_page.icon = 'check'
			self.ids.refresh_id_page2.icon = 'wifi'
			self.ids.infos_status.text = '[color=#0d6efd]Dati inviati con [/color][color=#32CD32]successo![/color]'
		except:
			pass
	def log_out(self,*args):
		Clock.unschedule(self.try_and_connect_api)
		global log_out_id
		log_out_id = 1
		self.ids.forms_number_profilo.text = ''
		self.ids.forms_number_delivered_profilo.text = ''
		self.manager.get_screen("pag1").ids.welcome_label.text = "[color=#0d6efd]Wel[/color][color=FFFFFF]come[/color]"
		self.manager.get_screen("pag1").ids.lock_state.active = False
		self.manager.get_screen("pag1").ids.user.helper_text = 'ID'
		self.manager.get_screen("pag1").ids.user.hint_text = 'User     '
		self.manager.get_screen("pag1").ids.user.mode = 'rectangle'
		self.manager.get_screen("pag1").ids.user.text = ''
		self.manager.get_screen("pag1").ids.password.text = ''
		self.manager.current = 'pag1'
		self.manager.transition.direction="left"


		

class TwoLineListItem(TwoLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")

class Pag3(Screen):
	def timing_for_ui(self,eq,carricatori,idx,non_x):
		global idx_command
		Clock.schedule_once(self.next_page_command, 0.7)
		self.manager.get_screen("pag2").ids.eq_id.text = str(eq)
		self.manager.get_screen("pag2").ids.carricatori.text = str(carricatori)
		idx_command = int(idx)
	def back_button_command_list(self,*args):
		Clock.schedule_once(self.next_page_command, 0.7)

	def next_page_command(self,*args):
		self.manager.current = 'pag2'
		self.manager.transition.direction="left"
		self.ids.container.clear_widgets()

	def timing_for_ui2(self,eq,carricatori,non_x):
		Clock.schedule_once(self.next_page_command, 0.7)
		self.manager.get_screen("pag2").ids.eq_id.text = str(eq)
		self.manager.get_screen("pag2").ids.carricatori.text = str(carricatori)

	def on_pre_enter(self, *args):
		user_id = self.manager.get_screen("pag1").ids.user.text # THIS IS HOW YOU TAKE INFOS FROM ANOTHER CLASSS!!!!!!!!!
		self.ids.welcome_orders.text = f"[color=#FFFF]{user_id.split('@')[0].capitalize()}[/color]"
		try:
			BASE ="127.0.0.1:5000"
			response = requests.get(BASE + f"/PATH_to_api/{user_id.split('@')[0]}/")
			x = response.json()
			conn = sqlite3.connect("modulo_app.db")
			if x == []:
				self.ids.container.add_widget(Label(text="[color=#0d6efd]Nes[/color]sun giri", font_name='data/font/RussoOne-Regular.ttf', markup=True,halign= "center",font_size= '25sp'))
			else:
			#------------------------------------DB
				c = conn.cursor()
				c.execute('DELETE FROM Command_Lists;',)
				for i in x:
					self.ids.container.add_widget(TwoLineListItem(text=f"EQ: {i['eq']}", secondary_text=f"Carricatori {i['carricatori']}", icon="images/box_id2.png", on_press=partial(self.timing_for_ui, i['eq'], i['carricatori'], i['id'])))

					#--------------------------------------------VERIFICARE
					c.execute("INSERT INTO Command_Lists VALUES (:eq, :carricatori, :status, :id_command)", {"eq":i['eq'], "carricatori":i['carricatori'], "status":0, "id_command":i['id']})
					conn.commit()
			conn.close()


		except Exception as e:
			#--------------------------------------------VERIFICARE
			# c.execute("UPDATE login_user_cookie SET sent_forms =?", (forms_number_id,))
			#--------------------------------------------VERIFICARE
			conn = sqlite3.connect("modulo_app.db")
			#------------------------------------DB
			c = conn.cursor()
			c.execute("SELECT * FROM Command_Lists WHERE status=:status", {"status": 0})
			# Verification step
			verification_step = c.fetchall()
			if verification_step == []:
				self.ids.container.add_widget(Label(text="[color=#0d6efd]Nes[/color]sun giri", font_name='data/font/RussoOne-Regular.ttf', markup=True,halign= "center",font_size= '25sp'))
			else:
				inx = 0
				for i in range(len(verification_step)):
					self.ids.container.add_widget(TwoLineListItem(text=f"EQ: {verification_step[inx][0]}", secondary_text=f"Carricatori {verification_step[inx][1]}", icon="images/box_id2.png", on_press=partial(self.timing_for_ui2, verification_step[inx][0], verification_step[inx][1])))
					inx +=1

			conn.close()
class WindowManager(ScreenManager):
    pass



class ModuloApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"


		return Builder.load_file("design_modulo.kv")





if __name__ == "__main__":
	ModuloApp().run()
