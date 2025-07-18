-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Jul 18, 2025 at 10:33 PM
-- Server version: 8.0.42
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `beautynailnet`
--

-- --------------------------------------------------------

--
-- Table structure for table `SERVICE`
--

CREATE TABLE `SERVICE` (
  `service_id` int NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `description` text,
  `base_price` decimal(8,2) NOT NULL,
  `duration_minutes` int NOT NULL,
  `category` varchar(50) NOT NULL,
  `requies_appointment` tinyint(1) DEFAULT '1'
) ;

--
-- Dumping data for table `SERVICE`
--

INSERT INTO `SERVICE` (`service_id`, `service_name`, `description`, `base_price`, `duration_minutes`, `category`, `requies_appointment`) VALUES
(1, 'Polish Change', 'Simple polish removal and new color application', 15.00, 20, 'Basic', 1),
(2, 'Cuticle Treatment', 'Professional cuticle care and conditioning', 20.00, 25, 'Treatment', 1),
(3, 'Paraffin Treatment', 'Moisturizing paraffin wax treatment for hands or feet', 25.00, 30, 'Treatment', 1),
(4, 'Gel Removal', 'Safe removal of existing gel polish', 12.00, 20, 'Removal', 1),
(5, 'Classic Manicure', 'Basic nail shaping, cuticle care, and polish application', 25.00, 45, 'Manicure', 1),
(6, 'Gel Manicure', 'Long-lasting gel polish application with UV curing', 35.00, 60, 'Manicure', 1),
(7, 'French Manicure', 'Classic white tip design with clear or nude base', 30.00, 50, 'Manicure', 1),
(8, 'Acrylic Full Set', 'Complete acrylic nail extension application', 55.00, 90, 'Extensions', 1),
(9, 'Classic Pedicure', 'Foot soak, nail care, and polish with relaxing massage', 40.00, 60, 'Pedicure', 1),
(10, 'Spa Pedicure', 'Deluxe pedicure with exfoliation and extended massage', 60.00, 75, 'Pedicure', 1),
(11, 'Nail Art Design', 'Custom artistic nail designs and decorations', 15.00, 30, 'Art', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `SERVICE`
--
ALTER TABLE `SERVICE`
  ADD PRIMARY KEY (`service_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `SERVICE`
--
ALTER TABLE `SERVICE`
  MODIFY `service_id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
