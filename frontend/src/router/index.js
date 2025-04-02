import { createRouter, createWebHashHistory } from 'vue-router';

import HomePage from '../pages/HomePage.vue';
import UserPage from '../pages/UserPage.vue';
import MealPage from '../pages/MealPage.vue';
import LoginPage from '../pages/LoginPage.vue';
import AddUser from '../pages/AddUser.vue';

const routes = [

    { path: '/', component: LoginPage },
    { path: '/home', component: HomePage, meta: { requiresAuth: true } },
    { path: '/user', component: UserPage, meta: { requiresAuth: true } },
    { path: '/meal', component: MealPage, meta: { requiresAuth: true } },
    { path: '/adduser', component: AddUser, meta: { requiresAuth: true } },

];

const router = createRouter ({
    history: createWebHashHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isLoggedIn = !!localStorage.getItem('user'); // Prüfen, ob Benutzer eingeloggt ist

    if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
        // Wenn Auth erforderlich ist und der Benutzer nicht eingeloggt ist
        next('/'); // Weiterleitung zur Login-Seite
    } else {
        next(); // Weiter zur gewünschten Seite
    }
});

export default router;