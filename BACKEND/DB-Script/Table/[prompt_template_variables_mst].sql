USE [ASISAI]
GO

/****** Object:  Table [dbo].[prompt_template_variables_mst]    Script Date: 06-03-2026 12:48:41 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[prompt_template_variables_mst](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[prompt_key] [varchar](100) NOT NULL,
	[keyword] [varchar](100) NOT NULL,
	[description] [varchar](255) NULL,
	[category] [varchar](50) NULL,
	[is_deleted] [bit] NOT NULL,
	[created_at] [datetime] NOT NULL,
	[updated_at] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[prompt_template_variables_mst] ADD  DEFAULT ((0)) FOR [is_deleted]
GO

ALTER TABLE [dbo].[prompt_template_variables_mst] ADD  DEFAULT (getdate()) FOR [created_at]
GO


