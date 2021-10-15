-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Ven 02 Juillet 2021 à 12:37
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `watchbot`
--

-- --------------------------------------------------------

--
-- Structure de la table `chat`
--

CREATE TABLE `chat` (
  `id` int(255) NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `iduser` int(255) NOT NULL,
  `text` text NOT NULL,
  `img` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(255) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `weight` int(11) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `idwatch` int(255) NOT NULL,
  `modelwatch` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `user`
--

INSERT INTO `user` (`id`, `gender`, `firstname`, `lastname`, `age`, `height`, `weight`, `mail`, `password`, `idwatch`, `modelwatch`) VALUES
(1, 'male', 'user1', 'user1', 25, 175, 75, 'user1@gmail.com', '$2y$10$WeTbkmoRtxMATMx3Ppq52ODaKsRA19FF0gEKOY1z0bsUse9IurBDa', 1, 'WatchBot Serie 1'),
(2, 'male', 'user2', 'user2', 22, 177, 77, 'user2@gmail.com', '$2y$10$1ZmUBfJiaofN83ooVSOq/.6W4D0pQeu8MtkzZDn9K8ZknNSc2ZHte', 2, 'WatchBot Serie 1'),
(3, 'female', 'user3', 'user3', 48, 168, 65, 'user3@gmail.com', '$2y$10$OYPfvTnasWK96izJfg5PVOFPYxquuDzAgA42QFRNzo1vNh77YqGtq', 3, 'WatchBot Serie 1'),
(4, 'female', 'user4', 'user4', 33, 175, 98, 'user4@gmail.com', '$2y$10$2Uu/8Uy/6pyOrWKhTb7JtOfolohDzmEBd0fnWw9OSrMdasu6q/HLW', 4, 'WatchBot Serie 1');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
