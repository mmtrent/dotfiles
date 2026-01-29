-- ~/.config/nvim/init.lua
-- ========== Basics ==========
vim.g.mapleader = " "
vim.g.maplocalleader = " "

local o = vim.opt
o.number = true
o.relativenumber = true
o.expandtab = true
o.shiftwidth = 2
o.tabstop = 2
o.termguicolors = true
o.cursorline = true
o.updatetime = 250
o.signcolumn = "yes"

-- ========== Bootstrap lazy.nvim ==========
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
	vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"https://github.com/folke/lazy.nvim.git",
		"--branch=stable",
		lazypath,
	})
end
vim.opt.rtp:prepend(lazypath)

-- ========== Plugins ==========
require("lazy").setup({
	-- Quality of life
	{ "folke/which-key.nvim", opts = {} },
	{ "numToStr/Comment.nvim", opts = {} },
	{ "kylechui/nvim-surround", version = "*", opts = {} },
	{ "windwp/nvim-autopairs", opts = {} },

	-- UI
	{
		"nvim-lualine/lualine.nvim",
		dependencies = { "nvim-tree/nvim-web-devicons" },
		opts = { options = { theme = "auto" } },
	},
	{ "lewis6991/gitsigns.nvim", opts = {} },
	{ "rose-pine/neovim", name = "rose-pine" },
	{ "neanias/everforest-nvim", name = "everforest" },
	{ "rebelot/kanagawa.nvim", name = "kanagawa" },

	-- Fuzzy finder
	{ "nvim-telescope/telescope.nvim", branch = "0.1.x", dependencies = { "nvim-lua/plenary.nvim" } },

	-- Treesitter
	{ "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },

	-- LSP / Tools
	{ "williamboman/mason.nvim", config = true },
	{ "williamboman/mason-lspconfig.nvim" },
	{ "neovim/nvim-lspconfig" },

	-- Completion
	{
		"hrsh7th/nvim-cmp",
		enabled = false,
		dependencies = {
			"L3MON4D3/LuaSnip",
			"saadparwaiz1/cmp_luasnip",
			"hrsh7th/cmp-nvim-lsp",
			"hrsh7th/cmp-buffer",
			"hrsh7th/cmp-path",
			"rafamadriz/friendly-snippets",
		},
	},

	-- Formatting (optional but nice)
	{
		"stevearc/conform.nvim",
		opts = {
			formatters_by_ft = {
				lua = { "stylua" },
				javascript = { "prettier" },
				typescript = { "prettier" },
				json = { "prettier" },
				python = { "black" },
				sh = { "shfmt" },
			},
			format_on_save = { timeout_ms = 500, lsp_fallback = true },
		},
	},
})

-- ========== Colors & UI ==========
vim.cmd.colorscheme("kanagawa-dragon")
require("lualine").setup({
	options = {
		theme = "kanagawa",
	},
})
require("gitsigns").setup({})

-- ========== Telescope keymaps ==========
local builtin = require("telescope.builtin")
vim.keymap.set("n", "<leader>ff", builtin.find_files, { desc = "Find files" })
vim.keymap.set("n", "<leader>fg", builtin.live_grep, { desc = "Live grep" })
vim.keymap.set("n", "<leader>fb", builtin.buffers, { desc = "Buffers" })
vim.keymap.set("n", "<leader>fh", builtin.help_tags, { desc = "Help" })

-- ========== Treesitter ==========
require("nvim-treesitter.configs").setup({
	ensure_installed = { "lua", "vim", "vimdoc", "bash", "python", "javascript", "typescript", "json", "markdown" },
	highlight = { enable = true },
	indent = { enable = true },
})
