-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2026 a las 03:10:38
-- Versión del servidor: 10.11.19-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hotel_prueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'Administrador hotel'),
(1, 'Recepcionista');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_group_permissions`
--

INSERT INTO `auth_group_permissions` (`id`, `group_id`, `permission_id`) VALUES
(10, 1, 28),
(1, 1, 32),
(2, 1, 36),
(3, 1, 37),
(4, 1, 40),
(5, 1, 42),
(6, 1, 44),
(7, 1, 48),
(8, 1, 49),
(9, 1, 52),
(22, 2, 25),
(23, 2, 26),
(24, 2, 28),
(25, 2, 30),
(11, 2, 32),
(12, 2, 36),
(13, 2, 37),
(14, 2, 38),
(15, 2, 40),
(16, 2, 41),
(17, 2, 42),
(18, 2, 44),
(19, 2, 48),
(20, 2, 49),
(21, 2, 52);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add habitacion', 7, 'add_habitacion'),
(26, 'Can change habitacion', 7, 'change_habitacion'),
(27, 'Can delete habitacion', 7, 'delete_habitacion'),
(28, 'Can view habitacion', 7, 'view_habitacion'),
(29, 'Can add cliente', 8, 'add_cliente'),
(30, 'Can change cliente', 8, 'change_cliente'),
(31, 'Can delete cliente', 8, 'delete_cliente'),
(32, 'Can view cliente', 8, 'view_cliente'),
(33, 'Can add estado reserva', 9, 'add_estadoreserva'),
(34, 'Can change estado reserva', 9, 'change_estadoreserva'),
(35, 'Can delete estado reserva', 9, 'delete_estadoreserva'),
(36, 'Can view estado reserva', 9, 'view_estadoreserva'),
(37, 'Can add huesped', 10, 'add_huesped'),
(38, 'Can change huesped', 10, 'change_huesped'),
(39, 'Can delete huesped', 10, 'delete_huesped'),
(40, 'Can view huesped', 10, 'view_huesped'),
(41, 'Can add reserva', 11, 'add_reserva'),
(42, 'Can change reserva', 11, 'change_reserva'),
(43, 'Can delete reserva', 11, 'delete_reserva'),
(44, 'Can view reserva', 11, 'view_reserva'),
(45, 'Can add historial reserva', 12, 'add_historialreserva'),
(46, 'Can change historial reserva', 12, 'change_historialreserva'),
(47, 'Can delete historial reserva', 12, 'delete_historialreserva'),
(48, 'Can view historial reserva', 12, 'view_historialreserva'),
(49, 'Can add reserva huesped', 13, 'add_reservahuesped'),
(50, 'Can change reserva huesped', 13, 'change_reservahuesped'),
(51, 'Can delete reserva huesped', 13, 'delete_reservahuesped'),
(52, 'Can view reserva huesped', 13, 'view_reservahuesped');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$smOu4gJPWCAjOhN2FXr9GW$x5tUFOi9VV4T7dYIlMiBezq1nRY/nN9awECfdYmzkl8=', '2026-11-16 01:20:25.000000', 1, 'robles', 'Boris', 'Robles', 'robles@gmail.com', 1, 0, '2026-11-13 20:08:21.000000'),
(2, 'pbkdf2_sha256$1000000$T1dwH3iFk5TCe2E0wvEpMf$+dqUWAREN9mkuTLY/BtHQcCYSw8p8JShbY/5MIJi3Xc=', '2026-11-16 01:54:45.165931', 0, 'recepcion1', 'Juan', 'Perez', '', 0, 1, '2026-11-13 20:20:21.000000'),
(3, 'pbkdf2_sha256$1000000$WuhLEIDdNiOxhefpx3MJvh$jmHTRXXCk2+wQmSE6gSzzwI1mhFMsMALUr6PiGu4ydI=', '2026-11-16 02:00:00.975166', 1, 'admin', 'Renata', 'Vera', '', 1, 1, '2026-11-13 20:26:31.000000'),
(4, 'pbkdf2_sha256$1000000$RFyg29HWTRubdsjzcizatj$csoHSscwGTV5kPplyvdhn4wok0DmUkvg/bAhI8MB92A=', '2026-11-16 01:28:13.655672', 0, 'admin2', 'Katherine', 'Scheel', '', 0, 1, '2026-11-16 01:14:17.722829');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 2, 1),
(2, 3, 2),
(3, 4, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-11-13 20:20:22.819005', '2', 'recepcion1', 1, '[{\"added\": {}}]', 4, 1),
(2, '2026-11-13 20:25:01.950441', '2', 'recepcion1', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(3, '2026-11-13 20:26:32.591793', '3', 'admin', 1, '[{\"added\": {}}]', 4, 1),
(4, '2026-11-13 20:27:00.773786', '3', 'admin', 2, '[{\"changed\": {\"fields\": [\"Groups\"]}}]', 4, 1),
(5, '2026-11-14 23:23:09.705387', '2', 'recepcion1', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 1),
(6, '2026-11-14 23:23:43.481785', '3', 'admin', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 1),
(7, '2026-11-16 01:14:18.409901', '4', 'admin2', 1, 'Cuenta creada desde el panel con el rol Administrador', 4, 3),
(8, '2026-11-16 01:20:59.178692', '3', 'admin', 2, '[{\"changed\": {\"fields\": [\"Staff status\", \"Superuser status\"]}}]', 4, 1),
(9, '2026-11-16 01:23:57.618188', '1', 'robles', 2, '[{\"changed\": {\"fields\": [\"Active\"]}}]', 4, 3),
(10, '2026-11-16 01:25:04.524829', '1', 'robles', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 4, 3),
(11, '2026-11-16 01:27:15.897521', '4', 'admin2', 2, 'Cuenta (Administrador) desactivada desde el panel', 4, 3),
(12, '2026-11-16 01:27:24.899661', '4', 'admin2', 2, 'Cuenta (Administrador) activada desde el panel', 4, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'habitaciones', 'habitacion'),
(8, 'reservas', 'cliente'),
(9, 'reservas', 'estadoreserva'),
(12, 'reservas', 'historialreserva'),
(10, 'reservas', 'huesped'),
(11, 'reservas', 'reserva'),
(13, 'reservas', 'reservahuesped'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-11-13 20:07:13.593184'),
(2, 'auth', '0001_initial', '2026-11-13 20:07:13.972802'),
(3, 'admin', '0001_initial', '2026-11-13 20:07:14.050509'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-11-13 20:07:14.060173'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-11-13 20:07:14.073707'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-11-13 20:07:14.140228'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-11-13 20:07:14.186702'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-11-13 20:07:14.212849'),
(9, 'auth', '0004_alter_user_username_opts', '2026-11-13 20:07:14.221938'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-11-13 20:07:14.268425'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-11-13 20:07:14.278056'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-11-13 20:07:14.333250'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-11-13 20:07:14.378159'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-11-13 20:07:14.401721'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-11-13 20:07:14.423976'),
(16, 'auth', '0011_update_proxy_permissions', '2026-11-13 20:07:14.435811'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-11-13 20:07:14.457330'),
(18, 'habitaciones', '0001_initial', '2026-11-13 20:07:14.478895'),
(19, 'reservas', '0001_initial', '2026-11-13 20:07:14.867954'),
(20, 'sessions', '0001_initial', '2026-11-13 20:07:14.896308');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2b3yu6okcx2g09w4794u4v3bqfsakmvu', '.eJxVjMsKgzAQAP9lzyWsZg3RY-_9Bsk-Um1LBKOn0n8vgof2OjPMG8a0b9O4V1vHWWEAD5dfxkmeVg6hj1Tui5OlbOvM7kjcaau7LWqv69n-DaZUJxigzZQCalb1GrouUG6ZFEVz7CJmEo1ixCJITcQ-onFL3tg3WXxvCJ8vAsU4iQ:1xSGhb:5xTZOwoUGVPft6jLi56p2P30dWc-_BCoaYjDGzr0IOs', '2026-11-14 16:35:07.610143'),
('5g0ruuvu7stczlw4f6tyoccdh5rf40fu', '.eJxVjMsKgzAQAP9lzyWsZg3RY-_9Bsk-Um1LBKOn0n8vgof2OjPMG8a0b9O4V1vHWWEAD5dfxkmeVg6hj1Tui5OlbOvM7kjcaau7LWqv69n-DaZUJxigzZQCalb1GrouUG6ZFEVz7CJmEo1ixCJITcQ-onFL3tg3WXxvCJ8vAsU4iQ:1xSm18:blR-0TPJAHM5Ahz3esuDADxyS7vGBCRjJuiUwLQk9DU', '2026-11-16 02:30:22.732786'),
('bfnr5omlueg9dp4jxd1eaa10tn24wlkp', '.eJxVjjsOgzAQBe-yNbIWbCNDmT5nsOzddUw-INmQJsrdIyKKpH0zGr0X-LCt2W9Vip8YRtDQ_G4x0E3mHfA1zJdF0TKvZYpqV9RBqzovLPfT4f4FcqgZRuiSCT1yYtbcW9ub1EXDSJycdZgMsSMxkQhN63BwKLEzWqJuE-lBEBp4TL5IlfIM36f2_QE2PD7B:1xSOJE:MxODUkVBa1wLEjw3UmheCuh_0vqL9u5XXdcBSl5rUsw', '2026-11-15 01:11:28.372653');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitaciones_habitacion`
--

CREATE TABLE `habitaciones_habitacion` (
  `id` bigint(20) NOT NULL,
  `numero` varchar(6) NOT NULL,
  `tipo` varchar(30) NOT NULL,
  `capacidad` smallint(5) UNSIGNED NOT NULL CHECK (`capacidad` >= 0),
  `precio_noche` int(10) UNSIGNED NOT NULL CHECK (`precio_noche` >= 0),
  `descripcion` varchar(255) NOT NULL,
  `estado` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `habitaciones_habitacion`
--

INSERT INTO `habitaciones_habitacion` (`id`, `numero`, `tipo`, `capacidad`, `precio_noche`, `descripcion`, `estado`) VALUES
(1, '101', 'Individual', 1, 35000, 'Cama de una plaza, baño privado', 'disponible'),
(2, '102', 'Matrimonial', 2, 55000, 'Cama de dos plazas, vista al río', 'disponible'),
(3, '201', 'Doble', 2, 50000, 'Dos camas de una plaza', 'disponible'),
(4, '202', 'Familiar', 4, 85000, 'Cama matrimonial y dos individuales', 'disponible'),
(5, '301', 'Suite', 6, 120000, 'Suite con tina y terraza', 'disponible');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_cliente`
--

CREATE TABLE `reservas_cliente` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_cliente`
--

INSERT INTO `reservas_cliente` (`id`, `nombre`, `apellido`, `documento`, `telefono`, `correo`) VALUES
(1, 'Juan', 'Perico', '24.505.211-4', '945632175', 'juanperico@gmail.com'),
(2, 'Josefa', 'Morales', '21.489.255-2', '978463152', 'josefamorales@gmail.com'),
(3, 'Boris', 'Pettet', '21.255.255-0', '+56975751919', 'boris@gmail.com'),
(4, 'Federico', 'Esparza', '21.155.255-1', '+56975757575', 'prueba@gmail.com'),
(5, 'Natalia', 'Mendez', '28.288.288-4', '+56945946325', 'natalia@gmail.com'),
(6, 'Gregorio', 'Sanchez', '12.344.455-1', '+56945682196', 'gregorio@gmail.com'),
(7, 'Prueba', 'Uno', '11.111.111-1', '+56915359743', 'pruebauno@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_estadoreserva`
--

CREATE TABLE `reservas_estadoreserva` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_estadoreserva`
--

INSERT INTO `reservas_estadoreserva` (`id`, `nombre`) VALUES
(5, 'Cancelada'),
(2, 'Confirmada'),
(3, 'En curso'),
(4, 'Finalizada'),
(1, 'Pendiente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_historialreserva`
--

CREATE TABLE `reservas_historialreserva` (
  `id` bigint(20) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `reserva_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_historialreserva`
--

INSERT INTO `reservas_historialreserva` (`id`, `accion`, `fecha`, `usuario_id`, `reserva_id`) VALUES
(1, 'Reserva creada', '2026-11-13 20:18:30.538049', NULL, 1),
(2, 'Reserva cancelada', '2026-11-13 20:30:17.856974', 2, 1),
(3, 'Reserva creada', '2026-11-13 20:32:22.278519', NULL, 2),
(4, 'Check-in realizado', '2026-11-13 20:33:11.776791', 2, 2),
(5, 'Pago registrado', '2026-11-13 20:35:51.411606', 2, 2),
(6, 'Check-out realizado', '2026-11-13 20:36:14.753869', 2, 2),
(7, 'Reserva creada', '2026-11-14 18:00:47.902926', NULL, 3),
(8, 'Reserva creada', '2026-11-14 18:44:14.128756', NULL, 4),
(9, 'Reserva creada', '2026-11-15 00:29:30.939917', NULL, 5),
(10, 'Reserva cancelada por el cliente', '2026-11-15 00:41:14.756157', NULL, 5),
(11, 'Reserva cancelada', '2026-11-15 15:16:41.746242', 2, 3),
(12, 'Reserva creada', '2026-11-15 15:33:30.115910', 2, 6),
(13, 'Pago registrado', '2026-11-15 16:08:04.333665', 3, 6),
(14, 'Check-in realizado', '2026-11-15 16:08:12.067027', 3, 6),
(15, 'Reserva creada', '2026-11-15 19:12:48.467262', NULL, 7),
(16, 'Reserva cancelada por el cliente', '2026-11-15 19:13:43.797732', NULL, 7),
(17, 'Reserva creada', '2026-11-16 01:33:47.078278', NULL, 8),
(18, 'Reserva cancelada por el cliente', '2026-11-16 01:34:56.622283', NULL, 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_huesped`
--

CREATE TABLE `reservas_huesped` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `documento` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_huesped`
--

INSERT INTO `reservas_huesped` (`id`, `nombre`, `apellido`, `documento`) VALUES
(1, 'Juan', 'Perico', '24.505.211-4'),
(2, 'Josefa', 'Morales', '21.489.255-2'),
(3, 'Boris', 'Pettet', '21.255.255-0'),
(4, 'Juan', 'Morales', '11.002.002-1'),
(5, 'Fernando', 'Morales', '11.111.222-1'),
(6, 'Yonatan', 'Perez', '21.255.244-0'),
(7, 'Federico', 'Esparza', '21.155.255-1'),
(8, 'Natalia', 'Mendez', '28.288.288-4'),
(9, 'Gregorio', 'Sanchez', '12.344.455-1'),
(10, 'Prueba', 'Uno', '11.111.111-1'),
(11, 'Prueba', 'Dos', '22.222.222-2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_reserva`
--

CREATE TABLE `reservas_reserva` (
  `id` bigint(20) NOT NULL,
  `codigo_reserva` varchar(20) NOT NULL,
  `fecha_entrada` date NOT NULL,
  `fecha_salida` date NOT NULL,
  `cantidad_personas` smallint(5) UNSIGNED NOT NULL CHECK (`cantidad_personas` >= 0),
  `precio_total` int(10) UNSIGNED NOT NULL CHECK (`precio_total` >= 0),
  `estado_pago` varchar(15) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_modificacion` datetime(6) NOT NULL,
  `cliente_id` bigint(20) NOT NULL,
  `estado_id` bigint(20) NOT NULL,
  `habitacion_id` bigint(20) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_reserva`
--

INSERT INTO `reservas_reserva` (`id`, `codigo_reserva`, `fecha_entrada`, `fecha_salida`, `cantidad_personas`, `precio_total`, `estado_pago`, `fecha_creacion`, `fecha_modificacion`, `cliente_id`, `estado_id`, `habitacion_id`, `usuario_id`) VALUES
(1, 'HRS-C524B3A8B98B', '2026-11-14', '2026-11-16', 2, 110000, 'pendiente', '2026-11-13 20:18:30.522581', '2026-11-13 20:30:17.854463', 1, 5, 2, NULL),
(2, 'HRS-878C8194E8B9', '2026-11-13', '2026-11-14', 2, 50000, 'pagado', '2026-11-13 20:32:22.270611', '2026-11-13 20:36:14.751993', 2, 4, 3, NULL),
(3, 'HRS-DCC2EED42A0E', '2026-11-20', '2026-11-22', 4, 170000, 'pendiente', '2026-11-14 18:00:47.867597', '2026-11-15 15:16:41.743666', 3, 5, 4, NULL),
(4, 'HRS-F2A32FB163E9', '2026-11-16', '2026-11-17', 1, 35000, 'pendiente', '2026-11-14 18:44:14.117850', '2026-11-14 18:44:14.117974', 4, 2, 1, NULL),
(5, 'HRS-C7C04A8356E1', '2026-11-16', '2026-11-17', 1, 55000, 'pendiente', '2026-11-15 00:29:30.933720', '2026-11-15 00:41:14.754203', 5, 5, 2, NULL),
(6, 'HRS-B68A4E2FA18F', '2026-11-15', '2026-11-16', 1, 35000, 'pagado', '2026-11-15 15:33:30.110310', '2026-11-15 16:08:12.065494', 6, 3, 1, 2),
(7, 'HRS-56F9F54AAC70', '2026-11-16', '2026-11-17', 1, 55000, 'pendiente', '2026-11-15 19:12:48.460684', '2026-11-15 19:13:43.795493', 5, 5, 2, NULL),
(8, 'HRS-C2FFA7F57B29', '2026-11-20', '2026-11-21', 2, 55000, 'pendiente', '2026-11-16 01:33:47.058765', '2026-11-16 01:34:56.621063', 7, 5, 2, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas_reservahuesped`
--

CREATE TABLE `reservas_reservahuesped` (
  `id` bigint(20) NOT NULL,
  `huesped_id` bigint(20) NOT NULL,
  `reserva_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reservas_reservahuesped`
--

INSERT INTO `reservas_reservahuesped` (`id`, `huesped_id`, `reserva_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 3),
(5, 5, 3),
(6, 6, 3),
(7, 7, 4),
(8, 8, 5),
(9, 9, 6),
(10, 8, 7),
(11, 10, 8),
(12, 11, 8);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `habitaciones_habitacion`
--
ALTER TABLE `habitaciones_habitacion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero` (`numero`);

--
-- Indices de la tabla `reservas_cliente`
--
ALTER TABLE `reservas_cliente`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `reservas_estadoreserva`
--
ALTER TABLE `reservas_estadoreserva`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `reservas_historialreserva`
--
ALTER TABLE `reservas_historialreserva`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reservas_historialreserva_usuario_id_0740e12f_fk_auth_user_id` (`usuario_id`),
  ADD KEY `reservas_historialre_reserva_id_efb80bc8_fk_reservas_` (`reserva_id`);

--
-- Indices de la tabla `reservas_huesped`
--
ALTER TABLE `reservas_huesped`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `reservas_reserva`
--
ALTER TABLE `reservas_reserva`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_reserva` (`codigo_reserva`),
  ADD KEY `reservas_reserva_cliente_id_78618bc5_fk_reservas_cliente_id` (`cliente_id`),
  ADD KEY `reservas_reserva_estado_id_5b91e46f_fk_reservas_estadoreserva_id` (`estado_id`),
  ADD KEY `reservas_reserva_habitacion_id_cedf2016_fk_habitacio` (`habitacion_id`),
  ADD KEY `reservas_reserva_usuario_id_531da18c_fk_auth_user_id` (`usuario_id`);

--
-- Indices de la tabla `reservas_reservahuesped`
--
ALTER TABLE `reservas_reservahuesped`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reserva_huesped_unico` (`reserva_id`,`huesped_id`),
  ADD KEY `reservas_reservahues_huesped_id_1d1f3d27_fk_reservas_` (`huesped_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `habitaciones_habitacion`
--
ALTER TABLE `habitaciones_habitacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `reservas_cliente`
--
ALTER TABLE `reservas_cliente`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `reservas_estadoreserva`
--
ALTER TABLE `reservas_estadoreserva`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `reservas_historialreserva`
--
ALTER TABLE `reservas_historialreserva`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `reservas_huesped`
--
ALTER TABLE `reservas_huesped`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `reservas_reserva`
--
ALTER TABLE `reservas_reserva`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `reservas_reservahuesped`
--
ALTER TABLE `reservas_reservahuesped`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `reservas_historialreserva`
--
ALTER TABLE `reservas_historialreserva`
  ADD CONSTRAINT `reservas_historialre_reserva_id_efb80bc8_fk_reservas_` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`),
  ADD CONSTRAINT `reservas_historialreserva_usuario_id_0740e12f_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `reservas_reserva`
--
ALTER TABLE `reservas_reserva`
  ADD CONSTRAINT `reservas_reserva_cliente_id_78618bc5_fk_reservas_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `reservas_cliente` (`id`),
  ADD CONSTRAINT `reservas_reserva_estado_id_5b91e46f_fk_reservas_estadoreserva_id` FOREIGN KEY (`estado_id`) REFERENCES `reservas_estadoreserva` (`id`),
  ADD CONSTRAINT `reservas_reserva_habitacion_id_cedf2016_fk_habitacio` FOREIGN KEY (`habitacion_id`) REFERENCES `habitaciones_habitacion` (`id`),
  ADD CONSTRAINT `reservas_reserva_usuario_id_531da18c_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `reservas_reservahuesped`
--
ALTER TABLE `reservas_reservahuesped`
  ADD CONSTRAINT `reservas_reservahues_huesped_id_1d1f3d27_fk_reservas_` FOREIGN KEY (`huesped_id`) REFERENCES `reservas_huesped` (`id`),
  ADD CONSTRAINT `reservas_reservahues_reserva_id_50432e3c_fk_reservas_` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
