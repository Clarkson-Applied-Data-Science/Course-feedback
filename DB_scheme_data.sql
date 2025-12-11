-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Dec 11, 2025 at 11:13 PM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `course_feedback`
--

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `courseID` int UNSIGNED NOT NULL,
  `courseName` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `departmentName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `semesterOffered` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `isSuggestedBy` int UNSIGNED DEFAULT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `instructor` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`courseID`, `courseName`, `description`, `departmentName`, `semesterOffered`, `isSuggestedBy`, `startDate`, `endDate`, `instructor`) VALUES
(1, 'Data Driven Decision Making', 'is a practical course that teaches students how to use data to inform and improve real-world decisions. The course covers the full decision-making pipeline: defining a problem, collecting and cleaning relevant data, exploring and visualizing trends, and applying basic statistical and analytical techniques to generate actionable insights. By the end of the course will be able to support organizational decisions with evidence-based recommendations and simple dashboard-style reports.', 'Data science', 'Fall', NULL, '2024-08-26', '2024-12-10', 3),
(2, 'Machine Learning', 'Machine Learning is an applied course focused on building computer systems that can learn from data and improve over time without being explicitly programmed for every task. Students will be introduced to core concepts such as supervised and unsupervised learning, model training and evaluation, overfitting and regularization, and the bias–variance tradeoff. The course typically covers key algorithms like linear and logistic regression, decision trees, random forests, k-means clustering, and basic neural networks, along with model performance metrics. ', 'Data science', 'Fall', NULL, '2024-08-26', '2024-12-10', 3),
(3, 'Business Analytics', 'Business Analytics is a course that focuses on using data, statistical methods, and analytical tools to solve real business problems and guide strategic decisions. The course emphasizes tools like spreadsheets, dashboards, and basic analytics software to build reports, visualizations, and simple forecasting models. By the end, learners will be able to turn raw business data into clear, actionable insights that support decision-making in areas such as customer behavior, pricing, resource allocation, and performance measurement.', 'Business Analytics', 'Spring', 2, '2024-08-26', '2024-12-10', NULL),
(5, 'Probablity and statistics', 'Probability and Statistics is a foundational course that introduces students to the basic concepts needed to reason about uncertainty and analyze data. The course covers probability rules, random variables, common probability distributions, expectation and variance, and ideas like independence and conditional probability. On the statistics side, students learn how to summarize data, construct and interpret confidence intervals, perform hypothesis tests, and build simple regression models.', 'Mathematics', 'Fall', 1, '2024-08-26', '2024-12-10', NULL),
(7, 'Deep learning', 'Deep Learning is an advanced course that focuses on neural networks and how they can learn complex patterns from large amounts of data. Students will study core architectures such as feedforward networks, convolutional neural networks (CNNs), recurrent neural networks (RNNs) and LSTMs, and modern approaches like transformers and attention mechanisms. The course covers key concepts including gradient descent, backpropagation, activation functions, regularization, and techniques to prevent overfitting.', 'Computer Science', 'Spring', NULL, '2025-12-05', '2025-12-26', 3),
(17, 'MBA New course', 'is a practical course that teaches students how to use data to inform and improve real-world decisions. The course covers the full decision-making pipeline: defining a problem, collecting and cleaning relevant data, exploring and visualizing trends, and applying basic statistical and analytical techniques to generate actionable insights. By the end of the course will be able to support organizational decisions with evidence-based recommendations and simple dashboard-style reports.', 'Business Analytics', NULL, 4, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE `feedbacks` (
  `feedbackID` int UNSIGNED NOT NULL,
  `feedbackText` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `dateGiven` date DEFAULT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uuid` int UNSIGNED NOT NULL,
  `courseID` int UNSIGNED NOT NULL,
  `rating` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `feedbacks`
--

INSERT INTO `feedbacks` (`feedbackID`, `feedbackText`, `dateGiven`, `status`, `uuid`, `courseID`, `rating`) VALUES
(2, 'Good course but pacing was a bit fast in the middle of the semester. Regardless this course was good. I would be happy if the topics were vast.', '2024-11-11', 'approved', 4, 1, 4),
(12, 'This is a good course. I enjoyed it.. I learned a lot. I is the base for NLP so take the course. It helps alot. You will enjoy it. I took it on spring.', '2025-12-11', 'pending', 4, 2, 5),
(13, 'This is a good course.It is from maths department. I enjoyed it.. I learned a lot. So take the course. It helps alot.  I took it on spring.', '2025-12-11', 'approved', 2, 17, 4),
(14, 'The course covers the full decision-making pipeline: defining a problem, collecting and cleaning relevant data, exploring and visualizing trends, and applying basic statistical and analytical techniques to generate actionable insights. ', '2025-12-11', 'pending', 4, 7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uuid` int UNSIGNED NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `graduationDate` date DEFAULT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uuid`, `name`, `password`, `email`, `timestamp`, `graduationDate`, `role`) VALUES
(1, 'Eden', '2bfefa2c092c105937136b297aa1f8ad', 'edenabdisa90@gmail.com', '2025-11-15 21:39:36', NULL, 'admin'),
(2, 'Abigya', '2bfefa2c092c105937136b297aa1f8ad', 'abigya@gmail.com', '2025-11-15 21:39:36', '2024-11-01', 'alumni'),
(3, 'Delilah', '2bfefa2c092c105937136b297aa1f8ad', 'delilah@gmail.com', '2025-11-15 21:39:36', NULL, 'instructor'),
(4, 'Sandhya', '2bfefa2c092c105937136b297aa1f8ad', 'sandhya@gmail.com', '2025-11-15 21:55:09', '2026-11-01', 'student');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`courseID`),
  ADD KEY `fk_course_suggested_by` (`isSuggestedBy`);

--
-- Indexes for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`feedbackID`),
  ADD KEY `idx_feedback_user` (`uuid`),
  ADD KEY `idx_feedback_course` (`courseID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uuid`),
  ADD UNIQUE KEY `uq_user_email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `courseID` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `feedbackID` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uuid` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `fk_course_suggested_by` FOREIGN KEY (`isSuggestedBy`) REFERENCES `users` (`uuid`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD CONSTRAINT `fk_feedback_course` FOREIGN KEY (`courseID`) REFERENCES `courses` (`courseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_feedback_user` FOREIGN KEY (`uuid`) REFERENCES `users` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
