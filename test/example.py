from customtkinter import CTkTabview, CTkLabel, CTkScrollableFrame, CTkFrame
import logging
from datetime import datetime,timedelta

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controller import Controller

logger = logging.getLogger(__name__)

class UsersTab(CTkTabview):
    def __init__(self, master, controller:'Controller', font, n_days = 7):
        logger.debug("Initializing Widget")
        CTkTabview.__init__(self, master, corner_radius=0)
        self.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.controller =  controller
        self.font = font
        self._segmented_button.configure(font=self.font, corner_radius=6)

        self._MAX_USERS_TAB = 5
        self.format_show = "%d/%m, %a"
        self.format_date = "%Y-%m-%d"
        self.current_tab = 0
        self._n_days = range(n_days)
        # XXX Problem with midnight
        self.date = datetime.today().date()
        self.inc_day = timedelta(days=1)
        
        self.content = dict() 
        self.update_users()

        # Color index
        self.index_color = 1
        logger.debug("Widget Initialized")


    def build_calendar(self):
        logger.debug("Building calendar for users")
        for user in self.users:
            total_meals = 0
            date = self.date
            tab = self.add(user)
            tab.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
            tab.grid_rowconfigure((0,1,3,4), weight=1)

            meals = self.controller.db.meal.get_between(
                user,
                date.strftime(self.format_date), 
                (date+timedelta(weeks=1)).strftime(self.format_date)
            )
   
            for i in self._n_days:
                day_frame = CTkScrollableFrame(
                    self.tab(user),
                    label_text=date.strftime(self.format_show),
                    label_font=self.font,
                    label_fg_color="#353535",
                    fg_color="#353535",
                )
                
                day_frame.grid(
                    row=0, 
                    rowspan=5, 
                    column=i, 
                    padx=5,
                    pady=(10,5),
                    sticky="nsew"
                )
                self.content[user].append([date.strftime(self.format_date), day_frame])

                total_meals += self.build_meal_frames(meals, date, day_frame)
                
                if not day_frame.children.keys():
                    day_frame._scrollbar.configure(hover=False)
                    day_frame.configure(
                        scrollbar_button_color="#353535",
                        scrollbar_button_hover_color="#353535"
                    )
                    
                date = date + self.inc_day

            logger.debug(f"Tab built successfully. Widgets meals for {user}: {total_meals} found")
                

    def build_meal_frames(self, meals, date, day_frame:CTkScrollableFrame):
        """
            Returns the number of meals
        """
        last_meal_id = None
        number_meals = 0
        # XXX this sucks, but I won't touch it
        for meal_id, username, recipe, ingredient, brand, quantity, type, hour, meal_date_hours in meals:
            meal_date = meal_date_hours.split(' ')[0]
            if meal_date != date.strftime(self.format_date):
                continue
            
            day_frame._scrollbar.configure(hover=True)
            if meal_id != last_meal_id:
                # meal info
                number_meals += 1
                meal_frame = CTkFrame(
                    day_frame, 
                    corner_radius=10,
                    fg_color=self.cget("fg_color")
                )
                meal_frame.pack(fill="both", expand=True, padx=5, pady=2)

                meal_label = CTkLabel(
                    meal_frame, 
                    text=f"{recipe}",
                    text_color="#1BC13F",
                    font=self.font,
                    wraplength=100
                )
                meal_label.pack(fill="both", expand=True, padx=5, pady=(5,0))

                type_label = CTkLabel(
                    meal_frame, 
                    text=f"{type} {hour}h",
                    text_color="#1BC13F",
                    font=self.font,
                    wraplength=100
                )
                type_label.pack(fill="both", expand=True, padx=5, pady=2)
                last_meal_id = meal_id
     

            if ingredient:
                # Show ingredients
                ingredient_label = CTkLabel(
                    meal_frame, 
                    text=f"{ingredient}, {quantity}g",
                    font=self.font,
                    wraplength=100
                )
                ingredient_label.pack(fill="both", expand=True, padx=5, pady=2)
        
        return number_meals
    

    def previous_week(self, event=None):
        logger.debug("Navigating to previous week")
        self.date = self.date - timedelta(weeks=1)
        self.update_week()


    def next_week(self, event=None):
        logger.debug("Navigating to next week")
        self.date = self.date + timedelta(weeks=1)
        self.update_week()        


    def update_week(self):
        logger.debug("Updating week view")
        user = self.get()
        date = self.date
        meals = self.controller.db.meal.get_between(
            user,
            date.strftime(self.format_date), 
            (date+timedelta(weeks=1)).strftime(self.format_date)
        )

        for i in self._n_days:
            _, day_frame = self.content[user][i]
            
            meal_frames = list(day_frame.children.values())
            for meal_frame in meal_frames:
                meal_frame.destroy()
            
            self.content[user][i][0] = date.strftime(self.format_date)
            day_frame.configure(label_text=date.strftime(self.format_show))
            self.build_meal_frames(meals, date, day_frame)
            
            day_frame._scrollbar.set(0, 1)
            if not day_frame.children.keys():
                day_frame._scrollbar.configure(hover=False)
                day_frame.configure(
                    scrollbar_button_color="#353535",
                    scrollbar_button_hover_color="#353535"
                )
            else:
                day_frame.configure(
                    scrollbar_button_color=['gray55', 'gray41'],
                    scrollbar_button_hover_color=['gray40', 'gray53']
                )

            date = date + self.inc_day

        logger.debug("Week view updated")
        

    def update_users(self):
        """
            Returns a list with the new users
        """
        logger.debug("Updating users list")
        self.users = [user[0] for user in self.controller.db.user.get_all()]    
        user_on_tabs = set(self.content.keys())
        new_users = list()

        for user in self.users:
            if user not in user_on_tabs:
                self.content[user] = []
                new_users.append(user)
                logger.info(f"User added: {user}")

        for user in user_on_tabs:
            if user not in self.users:
                for _, frame in self.content[user]:
                    frame.destroy()
                
                del self.content[user]
                self.delete(user)
                logger.info(f"User removed: {user}")
                
        return new_users


    def build_new_tabs(self):
        logger.debug("Building new user tabs")
        new_user = self.update_users()
        for user in self.users:
            if user not in new_user:
                continue

            date = self.date
            tab = self.add(user)
            tab.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
            tab.grid_rowconfigure((0,1,3,4), weight=1)

            for i in self._n_days:
                day_frame = CTkScrollableFrame(
                    self.tab(user),
                    label_text=date.strftime(self.format_show),
                    label_font=self.font,
                    label_fg_color="#353535",
                    fg_color="#353535",
                    scrollbar_button_color="#353535",
                    scrollbar_button_hover_color="#353535"
                )
                day_frame._scrollbar.configure(hover=False)
                day_frame.grid(
                    row=0, 
                    rowspan=5, 
                    column=i, 
                    padx=5,
                    pady=(10,5),
                    sticky="nsew"
                )
                
                self.content[user].append([date.strftime(self.format_date), day_frame])
                date = date + self.inc_day

        logger.debug("New user tabs built successfully")


    def next_tab(self, event=None):
        self.current_tab = (self.current_tab + 1) % len(self.users)
        self.set(self.users[self.current_tab])
        logger.debug(f"Switched to next tab: {self.users[self.current_tab]}")

    def previous_tab(self, event=None):
        self.current_tab = (self.current_tab - 1)  % len(self.users)
        self.set(self.users[self.current_tab])
        logger.debug(f"Switched to previous tab: {self.users[self.current_tab]}")